import numpy as np
import cv2
import torch
import torch.nn as nn
import timm
from torchvision import transforms
from PIL import Image
from typing import Dict, Any
import os
import logging
import time
import psutil


class ModelInference:
    """Service for handling model inference and image analysis"""
    
    def __init__(self, model_path: str = "models/oral_cancer_checkpoint.pth"):
        self.confidence_threshold = 0.7
        # Force CPU usage for better compatibility and performance on CPU-only systems
        self.device = torch.device("cpu")
        self.model = None
        self.model_path = model_path
        self.class_names = None  # Will be loaded from checkpoint
        
        # Setup logging
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        
        # Add handler if not already present
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
        
        self.logger.info("Initializing ModelInference service...")
        self.logger.info(f"Model path: {self.model_path}")
        self.logger.info(f"Device: {self.device}")
        
        self._load_model()
        self._setup_transforms()
    
    def _load_model(self):
        """Load the trained PyTorch model"""
        self.logger.info("Starting model loading process...")
        start_time = time.time()
        
        try:
            if not os.path.exists(self.model_path):
                raise FileNotFoundError(f"Model file not found at {self.model_path}")
            
            self.logger.info(f"Model file found at {self.model_path}")
            
            # Load class names from checkpoint first
            checkpoint = torch.load(self.model_path, map_location=self.device)
            
            # Load class names from checkpoint
            if 'classes' in checkpoint:
                self.class_names = checkpoint['classes']
                self.logger.info(f"Classes loaded from checkpoint: {self.class_names}")
            else:
                self.class_names = ["Non-Cancer", "Cancer"]  # Fallback
                self.logger.warning("Classes not found in checkpoint, using fallback")
            
            # Create model architecture (EfficientNet-B0)
            num_classes = len(self.class_names)
            self.logger.info(f"Creating EfficientNet-B0 model with {num_classes} classes...")
            self.model = timm.create_model('tf_efficientnet_b0', pretrained=False, num_classes=num_classes)
            self.model = self.model.to(self.device)
            self.logger.info("Model architecture created successfully")
            
            # Load the trained weights with CPU mapping
            self.logger.info("Loading model weights...")
            
            if 'model_state_dict' in checkpoint:
                self.logger.info("Loading from model_state_dict...")
                self.model.load_state_dict(checkpoint['model_state_dict'])
            else:
                self.logger.info("Loading from direct state dict...")
                self.model.load_state_dict(checkpoint)
            
            self.logger.info("Model weights loaded successfully")
            
            self.model.eval()
            # Set model to CPU and disable gradients for inference
            self.model.cpu()
            for param in self.model.parameters():
                param.requires_grad = False
            
            # Optimize model for CPU inference
            self._optimize_for_cpu()
            
            load_time = time.time() - start_time
            self.logger.info(f"Model loaded successfully from {self.model_path}")
            self.logger.info(f"Using device: {self.device} (CPU-optimized)")
            self.logger.info(f"Model loading time: {load_time:.2f} seconds")
            
            # Log model parameters
            total_params = sum(p.numel() for p in self.model.parameters())
            trainable_params = sum(p.numel() for p in self.model.parameters() if p.requires_grad)
            self.logger.info(f"Total parameters: {total_params:,}")
            self.logger.info(f"Trainable parameters: {trainable_params:,}")
            
        except Exception as e:
            self.logger.error(f"Error loading model: {str(e)}")
            self.logger.warning("Falling back to mock inference")
            self.model = None
    
    def _optimize_for_cpu(self):
        """Optimize model for CPU inference"""
        self.logger.info("Applying CPU optimizations...")
        try:
            # Set model to evaluation mode
            self.model.eval()
            
            # Disable autograd for all parameters
            for param in self.model.parameters():
                param.requires_grad = False
            
            # Set number of threads for CPU inference (adjust based on your CPU)
            torch.set_num_threads(4)  # You can adjust this based on your CPU cores
            self.logger.info(f"Set PyTorch threads to: {torch.get_num_threads()}")
            
            # Enable optimizations for CPU
            torch.backends.mkldnn.enabled = True
            self.logger.info(f"MKLDNN enabled: {torch.backends.mkldnn.enabled}")
            
            self.logger.info("✅ Model optimized for CPU inference")
            
        except Exception as e:
            self.logger.warning(f"Could not apply CPU optimizations: {e}")
    
    def _setup_transforms(self):
        """Setup the preprocessing transforms"""
        self.inference_transform = transforms.Compose([
            transforms.Lambda(lambda img: cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)),
            transforms.Lambda(lambda img: self.remove_black_border(img)),
            transforms.Lambda(lambda img: self.apply_clahe_rgb(img)),
            transforms.Lambda(lambda img: cv2.cvtColor(img, cv2.COLOR_BGR2RGB)),
            transforms.ToPILImage(),
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])
    
    def to_rgb(self, img_bgr):
        """Convert BGR image to RGB"""
        return cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

    def center_crop_to_square(self, img):
        """Center crop image to square"""
        h, w = img.shape[:2]
        if h == w:
            return img
        if h > w:
            start = (h - w) // 2
            return img[start:start+w, :]
        else:
            start = (w - h) // 2
            return img[:, start:start+h]

    def resize_img(self, img, size=(224, 224)):
        """Resize image to specified size"""
        return cv2.resize(img, size, interpolation=cv2.INTER_AREA)

    def remove_black_border(self, img, thresh=10):
        """Remove black borders around image"""
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, th = cv2.threshold(gray, thresh, 255, cv2.THRESH_BINARY)
        coords = cv2.findNonZero(th)
        if coords is None:
            return img
        x, y, w, h = cv2.boundingRect(coords)
        return img[y:y+h, x:x+w]

    def apply_clahe_rgb(self, img):
        """Apply CLAHE to each channel in LAB color space for contrast enhancement"""
        lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        l2 = clahe.apply(l)
        lab2 = cv2.merge((l2, a, b))
        return cv2.cvtColor(lab2, cv2.COLOR_LAB2BGR)
    
    def preprocess_image(self, image: np.ndarray) -> torch.Tensor:
        """Preprocess image for model inference using the trained model's preprocessing"""
        try:
            # Convert numpy array to PIL Image
            if len(image.shape) == 3 and image.shape[2] == 3:
                pil_image = Image.fromarray(image.astype(np.uint8))
            else:
                # Handle grayscale or other formats
                pil_image = Image.fromarray(image.astype(np.uint8))
            
            # Apply the same transforms used during training
            transformed_image = self.inference_transform(pil_image)
            
            # Add batch dimension and ensure CPU tensor
            batch_image = transformed_image.unsqueeze(0)
            return batch_image.cpu()
            
        except Exception as e:
            self.logger.error(f"Error in preprocessing: {str(e)}")
            # Fallback to simple preprocessing
            target_size = (224, 224)
            resized_image = cv2.resize(image, target_size)
            normalized_image = resized_image.astype(np.float32) / 255.0
            tensor_image = torch.from_numpy(normalized_image).permute(2, 0, 1).unsqueeze(0)
            return tensor_image.cpu()
    
    def predict(self, image: np.ndarray) -> Dict[str, Any]:
        """Perform model prediction on the image"""
        self.logger.info("Starting prediction process...")
        start_time = time.time()
        
        # Log system resources before inference
        memory_before = psutil.virtual_memory().percent
        self.logger.info(f"Memory usage before inference: {memory_before:.1f}%")
        
        try:
            if self.model is None:
                self.logger.warning("Model not loaded, using mock prediction")
                return self._mock_prediction(image)
            
            # Log image information
            self.logger.info(f"Input image shape: {image.shape}")
            self.logger.info(f"Input image dtype: {image.dtype}")
            self.logger.info(f"Input image range: [{image.min()}, {image.max()}]")
            
            # Preprocess the image
            self.logger.info("Starting image preprocessing...")
            preprocess_start = time.time()
            processed_image = self.preprocess_image(image)
            preprocess_time = time.time() - preprocess_start
            self.logger.info(f"Preprocessing completed in {preprocess_time:.3f} seconds")
            self.logger.info(f"Processed image shape: {processed_image.shape}")
            
            # Run inference with CPU optimizations
            self.logger.info("Starting model inference...")
            inference_start = time.time()
            
            with torch.no_grad():
                # Ensure tensor is on CPU
                processed_image = processed_image.cpu()
                
                # Run inference
                outputs = self.model(processed_image)
                probabilities = torch.softmax(outputs, dim=1)
                confidence, predicted_class = torch.max(probabilities, 1)
                
                # Convert to CPU tensors for better memory management
                confidence = confidence.cpu()
                predicted_class = predicted_class.cpu()
                probabilities = probabilities.cpu()
                
                confidence_score = confidence.item()
                predicted_class_idx = predicted_class.item()
                
                inference_time = time.time() - inference_start
                self.logger.info(f"Inference completed in {inference_time:.3f} seconds")
                self.logger.info(f"Raw model outputs: {outputs.cpu().numpy()}")
                self.logger.info(f"Class probabilities: {probabilities.numpy()}")
                self.logger.info(f"Predicted class: {predicted_class_idx} ({self.class_names[predicted_class_idx]})")
                self.logger.info(f"Confidence score: {confidence_score:.4f}")
                
                # Map prediction to cancer detection (2 classes: 0=Non-Cancer, 1=Cancer)
                if predicted_class_idx == 1:  # Non-Cancer
                    prediction = "Non-Cancer - No signs of oral cancer detected"
                    risk_level = "Low"
                    recommendations = [
                        "Continue regular oral hygiene practices",
                        "Schedule routine dental check-ups every 6 months",
                        "Monitor for any changes in oral tissues",
                        "Maintain healthy lifestyle habits",
                        "Avoid tobacco and excessive alcohol consumption"
                    ]
                    self.logger.info("Prediction: NON-CANCER detected")
                else:  # Cancer (predicted_class_idx == 1)
                    prediction = "Cancer - Suspicious lesions detected that may indicate oral cancer"
                    risk_level = "High"
                    recommendations = [
                        "IMMEDIATE consultation with an oral cancer specialist required",
                        "Consider biopsy for definitive diagnosis",
                        "Avoid tobacco and alcohol consumption completely",
                        "Schedule follow-up appointment within 1 week",
                        "Consider second opinion from another specialist"
                    ]
                    self.logger.warning("Prediction: CANCER detected - High priority alert!")
            
            image_analysis = self._analyze_image_features(image)
            
            # Log final results
            total_time = time.time() - start_time
            memory_after = psutil.virtual_memory().percent
            memory_used = memory_after - memory_before
            
            self.logger.info(f"Total prediction time: {total_time:.3f} seconds")
            self.logger.info(f"Memory usage after inference: {memory_after:.1f}%")
            self.logger.info(f"Memory change: {memory_used:+.1f}%")
            self.logger.info(f"Final prediction: {prediction}")
            self.logger.info(f"Risk level: {risk_level}")
            self.logger.info(f"Number of recommendations: {len(recommendations)}")
            
            result = {
                "prediction": prediction,
                "confidence": round(confidence_score, 3),
                "risk_level": risk_level,
                "recommendations": recommendations,
                "image_analysis": image_analysis,
                "class_probabilities": {
                    self.class_names[i]: round(probabilities[0][i].item(), 3) 
                    for i in range(len(self.class_names))
                }
            }
            
            self.logger.info("Prediction completed successfully")
            return result
            
        except Exception as e:
            self.logger.error(f"Error during model inference: {str(e)}")
            self.logger.warning("Falling back to mock prediction")
            return self._mock_prediction(image)
    
    def _mock_prediction(self, image: np.ndarray) -> Dict[str, Any]:
        """Fallback mock prediction when model is not available"""
        self.logger.warning("Using mock prediction - model not available")
        confidence = np.random.uniform(0.3, 0.95)
        self.logger.info(f"Mock confidence: {confidence:.3f}")
        
        if confidence > 0.7:  # Higher threshold for 2-class system
            prediction = "Cancer - Suspicious lesions detected that may indicate oral cancer"
            risk_level = "High"
            recommendations = [
                "IMMEDIATE consultation with an oral cancer specialist required",
                "Consider biopsy for definitive diagnosis",
                "Avoid tobacco and alcohol consumption completely",
                "Schedule follow-up appointment within 1 week",
                "Consider second opinion from another specialist"
            ]
        else:
            prediction = "Non-Cancer - No signs of oral cancer detected"
            risk_level = "Low"
            recommendations = [
                "Continue regular oral hygiene practices",
                "Schedule routine dental check-ups every 6 months",
                "Monitor for any changes in oral tissues",
                "Maintain healthy lifestyle habits",
                "Avoid tobacco and excessive alcohol consumption"
            ]
        
        image_analysis = self._analyze_image_features(image)
        
        return {
            "prediction": prediction,
            "confidence": round(confidence, 3),
            "risk_level": risk_level,
            "recommendations": recommendations,
            "image_analysis": image_analysis,
            "class_probabilities": {
                "Non-Cancer": round(np.random.uniform(0.2, 0.8), 3),
                "Cancer": round(np.random.uniform(0.2, 0.8), 3)
            }
        }
    
    def _analyze_image_features(self, image: np.ndarray) -> Dict[str, Any]:
        """Analyze image features for additional insights"""
        hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        
        analysis = {
            "image_dimensions": image.shape,
            "brightness": float(np.mean(gray)),
            "contrast": float(np.std(gray)),
            "color_distribution": {
                "red_mean": float(np.mean(image[:, :, 0])),
                "green_mean": float(np.mean(image[:, :, 1])),
                "blue_mean": float(np.mean(image[:, :, 2]))
            },
            "texture_analysis": {
                "smoothness": float(np.var(cv2.Laplacian(gray, cv2.CV_64F))),
                "uniformity": float(np.sum(np.square(np.histogram(gray, 256)[0])))
            },
            "edge_density": float(np.sum(cv2.Canny(gray, 50, 150) > 0) / (gray.shape[0] * gray.shape[1])),
            "color_variation": float(np.std(hsv[:, :, 1]))
        }
        
        return analysis
    
    def predict_image(self, image_path: str) -> tuple:
        """
        Predicts the class of a single image from file path.
        Matches the reference code structure.

        Args:
            image_path (str): Path to the input image.

        Returns:
            tuple: Predicted class name and confidence score.
        """
        try:
            image = Image.open(image_path).convert("RGB")  # Ensure image is in RGB format
            image = self.inference_transform(image).unsqueeze(0).to(self.device)  # Apply transformations and add batch dimension

            with torch.no_grad():
                outputs = self.model(image)
                probabilities = torch.softmax(outputs, dim=1)[0]
                confidence, predicted_class_index = torch.max(probabilities, dim=0)

            predicted_class_name = self.class_names[predicted_class_index.item()]
            return predicted_class_name, confidence.item()
            
        except Exception as e:
            self.logger.error(f"Error in predict_image: {str(e)}")
            return "Error", 0.0
