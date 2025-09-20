// Libraries Imports
import React, { useState } from "react";
import {
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
  Image,
  ScrollView,
  TextInput,
  Alert,
  ActivityIndicator,
} from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import { Formik } from "formik";
import * as ImagePicker from "expo-image-picker";
import { Ionicons } from "@expo/vector-icons";
import * as Animatable from "react-native-animatable";
import { useRouter } from "expo-router";
import axios from "axios";
// Local Imports
import { questions } from "../data/data";
import { DetailsFromTypes } from "@/types/details";
import { validationSchema } from "@/validation/details";

export default function DetailsScreen() {
  const [imageUri, setImageUri] = useState<string | null>(null);
  const [focusedField, setFocusedField] = React.useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  const pickImage = async (
    setFieldValue: (field: keyof DetailsFromTypes, value: any) => void
  ) => {
    let result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ["images"],
      allowsEditing: true,
      allowsMultipleSelection: false,
      quality: 0.7,
    });

    if (!result.canceled) {
      const asset = result.assets[0];
      const uri = asset.uri;
      const mimeType = asset.mimeType;
      const fileSize = asset.fileSize;

      if (fileSize && fileSize > 1024 * 1024) {
        alert("Please upload only 1 MB or smaller images.");
        return;
      }

      if (
        mimeType !== "image/jpeg" &&
        mimeType !== "image/jpg" &&
        mimeType !== "image/png"
      ) {
        alert("Please select only JPG, JPEG, and PNG type image.");
        return;
      }

      setImageUri(uri);
      setFieldValue("file", uri);
    }
  };

  return (
    <SafeAreaView style={styles.safeArea}>
      <ScrollView contentContainerStyle={styles.container}>
        <Animatable.View
          animation="fadeInDown"
          duration={1000}
          style={styles.header}
        >
          <Text style={styles.title}>Oral Health Check</Text>
          <View style={styles.divider} />
        </Animatable.View>
        <Formik<DetailsFromTypes>
          initialValues={{
            name: "",
            age: "",
            gender: "",
            medical_history: "",
            additional_context: "",
            q1: "",
            q2: "",
            q3: "",
            q4: "",
            q5: "",
            file: "",
          }}
          validationSchema={validationSchema}
          onSubmit={async (values, { resetForm }) => {
            try {
              setLoading(true);
              let imageData = null;
              if (values.file) {
                try {
                  const fileUri = values.file;
                  const fileExtension =
                    fileUri.split(".").pop()?.toLowerCase() || "jpg";
                  const mimeType =
                    fileExtension === "png" ? "image/png" : "image/jpeg";
                  const filename = `oral_image_${Date.now()}.${fileExtension}`;

                  const formData = new FormData();
                  formData.append("file", {
                    uri: fileUri,
                    name: filename,
                    type: mimeType,
                  } as any);

                  // Upload to server
                  const imageRes = await axios.post(
                    "http://192.168.43.141:8000/detection/analyze",
                    formData,
                    {
                      headers: {
                        "Content-Type": "multipart/form-data",
                      },
                      timeout: 25000,
                    }
                  );

                  imageData = imageRes.data;
                } catch {
                  Alert.alert(
                    "Upload Failed",
                    "Could not upload image. Please try again."
                  );
                  return;
                } finally {
                  setLoading(false);
                }
              }

              const answers = questions.map((q, index) => ({
                question_id: `q${index + 1}`,
                question_text: q,
                answer: values[`q${index + 1}` as keyof typeof values],
              }));

              const questionnairePayload = {
                patient_info: {
                  name: values.name,
                  age: values.age ? Number(values.age) : null,
                  gender: values.gender.toLowerCase(),
                  medical_history: values.medical_history
                    ? values.medical_history.split(",").map((h) => h.trim())
                    : [],
                },
                answers,
                additional_context: values.additional_context,
              };
              setLoading(true);
              const qRes = await axios.post(
                "http://192.168.43.141:8000/questionnaire/analyze",
                questionnairePayload,
                { headers: { "Content-Type": "application/json" } }
              );

              resetForm();
              if (imageUri) {
                setImageUri(null);
              }

              router.push({
                pathname: "./report",
                params: {
                  imageResult: JSON.stringify(imageData),
                  questionnaireResult: JSON.stringify(qRes.data),
                },
              });
            } catch {
              Alert.alert("Error", "Submission failed. Please try again.");
            } finally {
              setLoading(false);
            }
          }}
        >
          {({
            handleChange,
            handleSubmit,
            setFieldValue,
            values,
            errors,
            touched,
          }) => (
            <View>
              <View style={styles.inputsWrapper}>
                <View style={styles.inputContainer}>
                  <Text style={styles.label}>Name:</Text>
                  <TextInput
                    style={[
                      styles.input,
                      focusedField === "name" && styles.inputFocused,
                    ]}
                    placeholder="Enter your name."
                    keyboardType="default"
                    placeholderTextColor="#b3b3b3"
                    onChangeText={handleChange("name")}
                    value={values.name}
                    onFocus={() => setFocusedField("name")}
                    onBlur={() => setFocusedField(null)}
                  />
                  {touched.name && errors.name && (
                    <Text style={styles.error}>{errors.name}</Text>
                  )}
                </View>
                <View style={styles.inputContainer}>
                  <Text style={styles.label}>Age:</Text>
                  <TextInput
                    style={[
                      styles.input,
                      focusedField === "age" && styles.inputFocused,
                    ]}
                    placeholder="Enter your age."
                    keyboardType="numeric"
                    placeholderTextColor="#b3b3b3"
                    onChangeText={handleChange("age")}
                    value={values.age}
                    onFocus={() => setFocusedField("age")}
                    onBlur={() => setFocusedField(null)}
                  />
                  {touched.age && errors.age && (
                    <Text style={styles.error}>{errors.age}</Text>
                  )}
                </View>
                <View style={styles.inputContainer}>
                  <Text style={styles.label}>Gender:</Text>
                  <TextInput
                    style={[
                      styles.input,
                      focusedField === "gender" && styles.inputFocused,
                    ]}
                    placeholder="Enter your gender."
                    keyboardType="default"
                    placeholderTextColor="#b3b3b3"
                    onChangeText={handleChange("gender")}
                    value={values.gender}
                    onFocus={() => setFocusedField("gender")}
                    onBlur={() => setFocusedField(null)}
                  />
                  {touched.gender && errors.gender && (
                    <Text style={styles.error}>{errors.gender}</Text>
                  )}
                </View>
                <View style={styles.inputContainer}>
                  <Text style={styles.label}>
                    Medical History (Comma Separated):
                  </Text>
                  <TextInput
                    style={[
                      styles.input,
                      focusedField === "medical_history" && styles.inputFocused,
                    ]}
                    placeholder="Enter your medical history."
                    keyboardType="default"
                    placeholderTextColor="#b3b3b3"
                    onChangeText={handleChange("medical_history")}
                    value={values.medical_history}
                    onFocus={() => setFocusedField("medical_history")}
                    onBlur={() => setFocusedField(null)}
                  />
                  {touched.medical_history && errors.medical_history && (
                    <Text style={styles.error}>{errors.medical_history}</Text>
                  )}
                </View>
                <View style={styles.inputContainer}>
                  <Text style={styles.label}>Extra Note:</Text>
                  <TextInput
                    style={[
                      styles.input,
                      focusedField === "additional_context" &&
                        styles.inputFocused,
                    ]}
                    placeholder="Enter any extra note."
                    keyboardType="default"
                    placeholderTextColor="#b3b3b3"
                    onChangeText={handleChange("additional_context")}
                    value={values.additional_context}
                    onFocus={() => setFocusedField("additional_context")}
                    onBlur={() => setFocusedField(null)}
                  />
                  {touched.additional_context && errors.additional_context && (
                    <Text style={styles.error}>
                      {errors.additional_context}
                    </Text>
                  )}
                </View>
              </View>
              {questions.map((q, index) => {
                const key = `q${index + 1}` as keyof DetailsFromTypes;
                return (
                  <View key={key} style={styles.questionBox}>
                    <Text style={styles.label}>{q}</Text>
                    <View style={styles.optionsRow}>
                      {(["Yes", "No"] as const).map((option) => (
                        <TouchableOpacity
                          key={option}
                          style={[
                            styles.option,
                            values[key] === option && styles.selectedOption,
                          ]}
                          onPress={() => setFieldValue(key, option)}
                        >
                          <Text
                            style={[
                              styles.optionText,
                              values[key] === option && styles.selectedText,
                            ]}
                          >
                            {option}
                          </Text>
                        </TouchableOpacity>
                      ))}
                    </View>
                    {touched[key] && errors[key] && (
                      <Text style={styles.error}>{errors[key]}</Text>
                    )}
                  </View>
                );
              })}
              <Text style={styles.label}>Upload Image</Text>
              <TouchableOpacity
                style={styles.imagePicker}
                onPress={() => pickImage(setFieldValue)}
              >
                {imageUri ? (
                  <Image source={{ uri: imageUri }} style={styles.image} />
                ) : (
                  <View style={styles.imagePlaceholder}>
                    <Ionicons name="camera" size={32} color="#2563eb" />
                    <Text style={styles.imagePlaceholderText}>
                      Tap to upload an image
                    </Text>
                  </View>
                )}
              </TouchableOpacity>
              {touched.file && errors.file && (
                <Text style={styles.error}>{errors.file}</Text>
              )}
              <TouchableOpacity
                style={styles.button}
                onPress={() => handleSubmit()}
              >
                {loading ? (
                  <ActivityIndicator color="#fff" />
                ) : (
                  <View
                    style={{
                      flexDirection: "row",
                      alignItems: "center",
                    }}
                  >
                    <Text style={styles.buttonText}>Submit Details</Text>
                    <Ionicons name="send" size={22} color="#fff" />
                  </View>
                )}
              </TouchableOpacity>
            </View>
          )}
        </Formik>
      </ScrollView>
    </SafeAreaView>
  );
}

// Styling
const styles = StyleSheet.create({
  safeArea: {
    flex: 1,
    backgroundColor: "#0d0d0d",
  },
  container: {
    flexGrow: 1,
    padding: 20,
    paddingTop: 16,
  },
  header: {
    alignItems: "center",
    marginBottom: 36,
  },
  title: {
    fontSize: 30,
    color: "#fff",
    fontFamily: "SpaceGrotesk-Medium",
    marginBottom: 28,
    textAlign: "center",
  },
  divider: {
    height: 3,
    width: 80,
    backgroundColor: "#2563eb",
    borderRadius: 2,
  },
  inputsWrapper: {
    marginBottom: 28,
  },
  inputContainer: {
    flexDirection: "column",
    gap: 5,
    marginBottom: 10,
  },
  input: {
    backgroundColor: "#1e1e1e",
    color: "#fff",
    borderWidth: 1,
    borderColor: "#2c2c2c",
    borderRadius: 12,
    paddingHorizontal: 14,
    paddingVertical: 12,
    fontSize: 16,
    fontFamily: "SpaceGrotesk-Medium",
  },
  inputFocused: {
    borderColor: "#2563eb",
  },
  questionBox: {
    marginBottom: 28,
  },
  label: {
    fontSize: 20,
    color: "#fff",
    marginRight: 8,
    fontFamily: "SpaceGrotesk-Medium",
    marginBottom: 12,
    lineHeight: 22,
  },
  optionsRow: {
    flexDirection: "row",
    justifyContent: "space-between",
  },
  option: {
    paddingVertical: 14,
    borderRadius: 12,
    backgroundColor: "#1e1e1e",
    borderWidth: 1,
    borderColor: "#2c2c2c",
    width: "48%",
    alignItems: "center",
  },
  selectedOption: {
    backgroundColor: "#2563eb",
    borderColor: "#2563eb",
  },
  optionText: {
    fontSize: 17,
    color: "#b3b3b3",
    fontFamily: "SpaceGrotesk-Medium",
  },
  selectedText: {
    color: "#fff",
    fontFamily: "SpaceGrotesk-Medium",
  },
  imagePicker: {
    height: 140,
    width: "100%",
    borderRadius: 16,
    borderWidth: 1,
    borderColor: "#2c2c2c",
    backgroundColor: "#1e1e1e",
    justifyContent: "center",
    alignItems: "center",
    marginTop: 12,
    marginBottom: 28,
    overflow: "hidden",
  },
  image: {
    height: "100%",
    width: "100%",
    borderRadius: 16,
  },
  imagePlaceholder: {
    alignItems: "center",
    justifyContent: "center",
  },
  imagePlaceholderText: {
    color: "#2563eb",
    marginTop: 8,
    fontSize: 14,
    fontFamily: "SpaceGrotesk-Medium",
  },
  error: {
    fontSize: 15,
    color: "#E63946",
    marginTop: 6,
    fontFamily: "SpaceGrotesk-Medium",
  },
  button: {
    backgroundColor: "#2563eb",
    borderRadius: 24,
    paddingVertical: 16,
    flexDirection: "row",
    justifyContent: "center",
    alignItems: "center",
    marginTop: 8,
    marginBottom: 24, // Added bottom margin for better spacing
  },
  buttonText: {
    color: "#fff",
    marginRight: 8,
    fontSize: 25,
    fontFamily: "SpaceGrotesk-Medium",
  },
});
