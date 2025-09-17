// Libraries Imports
import React, { useState } from "react";
import {
  View,
  Text,
  TouchableOpacity,
  StyleSheet,
  Image,
  ScrollView,
} from "react-native";
import { Formik } from "formik";
import * as ImagePicker from "expo-image-picker";
import { Ionicons } from "@expo/vector-icons";
import * as Animatable from "react-native-animatable";
import { useRouter } from "expo-router";
// Local Imports
import { questions } from "../data/data";
import { FormValues } from "@/types/form";
import { validationSchema } from "@/validation/form";

export default function DetailsScreen() {
  const [imageUri, setImageUri] = useState<string | null>(null);
  const router = useRouter();

  const pickImage = async (
    setFieldValue: (field: keyof FormValues, value: any) => void
  ) => {
    let result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ["images"],
      allowsEditing: true,
      allowsMultipleSelection: false,
      quality: 0.7,
    });

    if (!result.canceled) {
      const uri = result.assets[0].uri;
      setImageUri(uri);
      setFieldValue("image", uri);
    }
  };

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Animatable.View
        animation="fadeInDown"
        duration={1000}
        style={styles.header}
      >
        <Text style={styles.title}>Oral Health Check</Text>
        <View style={styles.divider} />
      </Animatable.View>
      <Formik<FormValues>
        initialValues={{
          q1: "",
          q2: "",
          q3: "",
          q4: "",
          q5: "",
          image: "",
        }}
        validationSchema={validationSchema}
        onSubmit={(values) => {
          const structured: Record<string, string> = {};

          questions.forEach((q, index) => {
            const key = `q${index + 1}` as keyof FormValues;
            structured[q] = values[key];
          });

          structured["Uploaded Image"] = values.image;
          router.navigate("./report");
          console.log("Submitted Data:", structured);
        }}
      >
        {({ handleSubmit, setFieldValue, values, errors, touched }) => (
          <>
            {questions.map((q, index) => {
              const key = `q${index + 1}` as keyof FormValues;
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
                <Ionicons name="image" size={40} color="#00BFA6" />
              )}
            </TouchableOpacity>
            {touched.image && errors.image && (
              <Text style={styles.error}>{errors.image}</Text>
            )}
            <TouchableOpacity
              style={styles.button}
              onPress={() => handleSubmit()}
            >
              <Ionicons name="send" size={22} color="#fff" />
              <Text style={styles.buttonText}>Submit Details</Text>
            </TouchableOpacity>
          </>
        )}
      </Formik>
    </ScrollView>
  );
}

// Styles
const styles = StyleSheet.create({
  container: {
    flexGrow: 1,
    padding: 24,
    backgroundColor: "#121212",
  },
  header: {
    alignItems: "center",
    marginBottom: 36,
    marginTop: 24,
  },
  title: {
    fontSize: 28,
    fontWeight: "700",
    color: "#ffffff",
    marginBottom: 28,
    textAlign: "center",
    letterSpacing: 0.5,
  },
  divider: {
    height: 3,
    width: 80,
    backgroundColor: "#00BFA6",
    borderRadius: 2,
  },
  questionBox: {
    marginBottom: 28,
  },
  label: {
    fontSize: 16,
    fontWeight: "500",
    color: "#e0e0e0",
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
    backgroundColor: "#00BFA6",
    borderColor: "#00BFA6",
  },
  optionText: {
    fontSize: 15,
    color: "#b3b3b3",
    fontWeight: "500",
  },
  selectedText: {
    color: "#fff",
    fontWeight: "700",
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
  },
  image: {
    height: "100%",
    width: "100%",
    borderRadius: 16,
  },
  error: {
    fontSize: 13,
    color: "#ff6b6b",
    marginTop: 6,
  },
  button: {
    backgroundColor: "#00BFA6",
    borderRadius: 24,
    paddingVertical: 16,
    flexDirection: "row",
    justifyContent: "center",
    alignItems: "center",
    marginTop: 8,
  },
  buttonText: {
    color: "#fff",
    fontSize: 18,
    fontWeight: "700",
    letterSpacing: 0.3,
    marginLeft: 8,
  },
});
