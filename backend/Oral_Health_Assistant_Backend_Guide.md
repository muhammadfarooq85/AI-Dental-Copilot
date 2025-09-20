# 🦷 Oral Health Assistant --- Backend Setup Guide

## ⚙️ Getting Started (Setup Instructions)

### 1. Clone the Repository

``` bash
git clone <your-repo-url>
cd <your-repo-folder>
```

### 2. Create and Activate a Virtual Environment

**On Windows**

``` bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux**

``` bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

``` bash
pip install -r requirements.txt
```

### 4. Install CPU Version of PyTorch

``` bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
```

### 5. Add Environment Variables

-   Place the provided `.env` file in the root directory of the project.

### 6. Add Model File

-   Place the provided `.pth` model file inside the `models/` folder
    (create it if it doesn't exist).

### 7. Run the Server

``` bash
python main.py
```

> The backend will start on: **http://localhost:8000**

------------------------------------------------------------------------

## 🚀 API Endpoints

### 🖼️ 1. Image Inference

**Endpoint**

    POST http://localhost:8000/detection/analyze

**Input** - multipart/form-data - Field: `image` → the image file to
analyze

**Output** - Inference results (detection output)

------------------------------------------------------------------------

### 📋 2. Questionnaire Analysis

**Endpoint**

    POST http://localhost:8000/questionnaire/analyze

**Example Request**

``` json
{
  "patient_info": {
    "name": "John Doe",
    "age": 35,
    "gender": "male",
    "medical_history": ["hypertension"]
  },
  "answers": [
    {
      "question_id": "q1",
      "question_text": "Do you have any sores or ulcers in your mouth?",
      "answer": "No"
    },
    {
      "question_id": "q2",
      "question_text": "Is there any swelling or redness in your mouth?",
      "answer": "Yes"
    },
    {
      "question_id": "q3",
      "question_text": "Are you experiencing any unusual pain in your mouth?",
      "answer": "Yes"
    },
    {
      "question_id": "q4",
      "question_text": "Have you noticed any changes in the inner lining of your mouth recently?",
      "answer": "No"
    },
    {
      "question_id": "q5",
      "question_text": "Have you noticed any lumps or thickened areas in your mouth or neck?",
      "answer": "Yes"
    }
  ],
  "additional_context": "Patient reported occasional bleeding gums during brushing."
}
```

**Output** - Risk assessment or diagnostic suggestions

------------------------------------------------------------------------

### 🦷 3. Find Nearby Dentists

**Endpoint**

    POST http://localhost:8000/dentist/find-dentists

**Example Request**

``` json
{
  "address": "123 street",
  "city": "New York",
  "state": "New Yor",
  "country": "USA",
  "radius_km": 10
}
```

**Output** - List of nearby dentists within the given radius

------------------------------------------------------------------------

## 📝 Notes

-   Make sure Python (\>=3.9) is installed.
-   Use the provided `.env` and `.pth` files as they are crucial for the
    backend to work.
-   The backend runs by default on port `8000`.
