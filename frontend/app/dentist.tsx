// Libraries Imports
import React, { useState } from "react";
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  ScrollView,
  ActivityIndicator,
  StyleSheet,
} from "react-native";
import { Formik } from "formik";
import axios from "axios";
import * as Animatable from "react-native-animatable";
import { SafeAreaView } from "react-native-safe-area-context";
import { Ionicons } from "@expo/vector-icons";
import { useRouter } from "expo-router";
// Local Imports
import { DetistFormTypes } from "@/types/dentist";
import { dentistValidationSchema } from "@/validation/dentist";

export default function FindDentistsScreen() {
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState<any[]>([]);
  const [focusedField, setFocusedField] = useState<string | null>(null);
  const router = useRouter();

  return (
    <SafeAreaView style={styles.safeArea}>
      <ScrollView contentContainerStyle={styles.container}>
        <Animatable.View
          animation="fadeInDown"
          duration={1000}
          style={styles.header}
        >
          <Text style={styles.title}>Find Nearby Dentists</Text>
          <View style={styles.divider} />
        </Animatable.View>
        <Formik<DetistFormTypes>
          initialValues={{
            address: "",
            city: "",
            state: "",
            country: "",
            radius_km: "10",
          }}
          validationSchema={dentistValidationSchema}
          onSubmit={async (values, { resetForm }) => {
            try {
              setLoading(true);
              const res = await axios.post(
                "http://192.168.43.141:8000/dentist/find-dentists",
                {
                  ...values,
                  radius_km: Number(values.radius_km),
                }
              );
              setResults(res.data.dentists || []);
              resetForm();
            } catch {
              alert("Something went wrong, please try again.");
            } finally {
              setLoading(false);
            }
          }}
        >
          {({
            handleChange,
            handleSubmit,
            handleBlur,
            values,
            errors,
            touched,
          }) => (
            <View>
              <View style={styles.inputContainer}>
                <Text style={styles.label}>Address:</Text>
                <TextInput
                  style={[
                    styles.input,
                    focusedField === "address" && styles.inputFocused,
                  ]}
                  placeholder="Enter Address"
                  placeholderTextColor="#b3b3b3"
                  value={values.address}
                  onChangeText={handleChange("address")}
                  onFocus={() => setFocusedField("address")}
                  onBlur={() => {
                    handleBlur("address");
                    setFocusedField(null);
                  }}
                />
                {touched.address && errors.address && (
                  <Text style={styles.error}>{errors.address}</Text>
                )}
              </View>
              <View style={styles.inputContainer}>
                <Text style={styles.label}>City:</Text>
                <TextInput
                  style={[
                    styles.input,
                    focusedField === "city" && styles.inputFocused,
                  ]}
                  placeholder="Enter City."
                  placeholderTextColor="#b3b3b3"
                  value={values.city}
                  onChangeText={handleChange("city")}
                  onFocus={() => setFocusedField("city")}
                  onBlur={() => {
                    handleBlur("city");
                    setFocusedField(null);
                  }}
                />
                {touched.city && errors.city && (
                  <Text style={styles.error}>{errors.city}</Text>
                )}
              </View>
              <View style={styles.inputContainer}>
                <Text style={styles.label}>State:</Text>
                <TextInput
                  style={[
                    styles.input,
                    focusedField === "state" && styles.inputFocused,
                  ]}
                  placeholder="Enter State."
                  placeholderTextColor="#b3b3b3"
                  value={values.state}
                  onChangeText={handleChange("state")}
                  onFocus={() => setFocusedField("state")}
                  onBlur={() => {
                    handleBlur("state");
                    setFocusedField(null);
                  }}
                />
                {touched.state && errors.state && (
                  <Text style={styles.error}>{errors.state}</Text>
                )}
              </View>
              <View style={styles.inputContainer}>
                <Text style={styles.label}>Country:</Text>
                <TextInput
                  style={[
                    styles.input,
                    focusedField === "country" && styles.inputFocused,
                  ]}
                  placeholder="Enter Country."
                  placeholderTextColor="#b3b3b3"
                  value={values.country}
                  onChangeText={handleChange("country")}
                  onFocus={() => setFocusedField("country")}
                  onBlur={() => {
                    handleBlur("country");
                    setFocusedField(null);
                  }}
                />
                {touched.country && errors.country && (
                  <Text style={styles.error}>{errors.country}</Text>
                )}
              </View>
              <View style={styles.inputContainer}>
                <Text style={styles.label}>Search Radius (km):</Text>
                <TextInput
                  style={[
                    styles.input,
                    focusedField === "radius_km" && styles.inputFocused,
                  ]}
                  placeholder="Enter radius."
                  placeholderTextColor="#b3b3b3"
                  keyboardType="numeric"
                  value={values.radius_km}
                  onChangeText={handleChange("radius_km")}
                  onFocus={() => setFocusedField("radius_km")}
                  onBlur={() => {
                    handleBlur("radius_km");
                    setFocusedField(null);
                  }}
                />
                {touched.radius_km && errors.radius_km && (
                  <Text style={styles.error}>{errors.radius_km}</Text>
                )}
              </View>
              <View style={styles.buttonRow}>
                <TouchableOpacity
                  style={styles.button}
                  onPress={() => router.navigate("/dentist")}
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
                      <Text
                        style={styles.buttonText}
                        onPress={() => handleSubmit()}
                      >
                        Search
                      </Text>
                      <Ionicons name="search" size={22} color="#fff" />
                    </View>
                  )}
                </TouchableOpacity>
                <TouchableOpacity
                  style={[styles.button, styles.secondaryBtn]}
                  onPress={() => router.navigate("/")}
                >
                  <Text style={styles.secondaryText}>Go Home</Text>
                  <Ionicons name="home" size={20} color="#2563eb" />
                </TouchableOpacity>
              </View>
            </View>
          )}
        </Formik>
        <View style={styles.resultsSection}>
          {results.length === 0 ? (
            <View style={styles.cardCentered}>
              <Text style={styles.cardTitle}>⚠️ No Dentist!</Text>
            </View>
          ) : (
            results.map((dentist, index) => (
              <View key={index} style={styles.card}>
                <View style={styles.cardHeader}>
                  <Text style={styles.cardTitle}>{dentist.name}</Text>
                  <View style={styles.ratingContainer}>
                    <Ionicons name="star" size={16} color="#FFD700" />
                    <Text style={styles.ratingText}>{dentist.rating}</Text>
                  </View>
                </View>

                <View style={styles.cardDetail}>
                  <Ionicons name="location-outline" size={16} color="#9ca3af" />
                  <Text style={styles.cardSubtitle}>{dentist.address}</Text>
                </View>

                <View style={styles.cardDetail}>
                  <Ionicons name="call-outline" size={16} color="#9ca3af" />
                  <Text style={styles.cardPhone}>{dentist.phone}</Text>
                </View>

                {dentist.website && (
                  <TouchableOpacity
                    style={styles.websiteButton}
                    onPress={() => router.navigate(dentist.website)}
                  >
                    <Ionicons name="globe-outline" size={16} color="#3b82f6" />
                    <Text style={styles.websiteText}>Visit Website</Text>
                  </TouchableOpacity>
                )}

                {dentist.distance && (
                  <View style={styles.distanceContainer}>
                    <Ionicons
                      name="navigate-outline"
                      size={14}
                      color="#00BFA6"
                    />
                    <Text style={styles.distanceText}>
                      {dentist.distance} away
                    </Text>
                  </View>
                )}
              </View>
            ))
          )}
        </View>
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
  inputContainer: {
    marginBottom: 12,
  },
  label: {
    color: "#fff",
    marginBottom: 6,
    fontSize: 20,
    fontFamily: "SpaceGrotesk-Medium",
  },
  input: {
    backgroundColor: "#1a1a1a",
    color: "#fff",
    borderRadius: 12,
    padding: 12,
    fontSize: 16,
    borderWidth: 1,
    borderColor: "#1a1a1a",
  },
  inputFocused: {
    borderColor: "#2563eb",
  },
  error: {
    fontSize: 15,
    color: "#E63946",
    marginTop: 6,
    fontFamily: "SpaceGrotesk-Medium",
  },
  buttonRow: {
    flexDirection: "column",
    justifyContent: "center",
    gap: 20,
    marginTop: 10,
  },
  button: {
    flex: 1,
    backgroundColor: "#2563eb",
    borderRadius: 20,
    paddingVertical: 14,
    flexDirection: "row",
    justifyContent: "center",
    alignItems: "center",
    marginHorizontal: 6,
  },
  buttonText: {
    color: "#fff",
    fontSize: 25,
    fontFamily: "SpaceGrotesk-Medium",
    marginRight: 8,
  },
  secondaryBtn: {
    backgroundColor: "transparent",
    borderWidth: 1,
    borderColor: "#2563eb",
  },
  secondaryText: {
    color: "#2563eb",
    fontSize: 25,
    fontFamily: "SpaceGrotesk-Medium",
    marginRight: 8,
  },
  buttonDisabled: {
    opacity: 0.6,
  },
  resultsSection: {
    marginTop: 24,
  },
  cardLink: {
    color: "#3b82f6",
    fontSize: 14,
    marginTop: 4,
    textDecorationLine: "underline",
  },
  resultsHeading: {
    fontSize: 18,
    fontWeight: "600",
    color: "#fff",
    marginBottom: 12,
  },
  noResults: {
    color: "#a1a1aa",
  },
  card: {
    backgroundColor: "rgba(255, 255, 255, 0.08)",
    padding: 20,
    borderRadius: 16,
    marginBottom: 16,
    borderWidth: 1,
    borderColor: "rgba(255, 255, 255, 0.1)",
  },
  cardHeader: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: 12,
  },
  cardTitle: {
    color: "#fff",
    fontWeight: "bold",
    fontSize: 18,
    flex: 1,
  },
  ratingContainer: {
    flexDirection: "row",
    alignItems: "center",
    backgroundColor: "rgba(255, 215, 0, 0.1)",
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 8,
  },
  ratingText: {
    color: "#FFD700",
    fontWeight: "600",
    marginLeft: 4,
    fontSize: 14,
  },
  cardDetail: {
    flexDirection: "row",
    alignItems: "center",
    marginBottom: 8,
  },
  cardSubtitle: {
    color: "#d4d4d8",
    fontSize: 14,
    marginLeft: 8,
    flex: 1,
  },
  cardPhone: {
    color: "#9ca3af",
    fontSize: 14,
    marginLeft: 8,
  },
  websiteButton: {
    flexDirection: "row",
    alignItems: "center",
    backgroundColor: "rgba(59, 130, 246, 0.1)",
    paddingHorizontal: 12,
    paddingVertical: 8,
    borderRadius: 8,
    alignSelf: "flex-start",
    marginTop: 8,
  },
  websiteText: {
    color: "#3b82f6",
    fontSize: 14,
    fontWeight: "500",
    marginLeft: 6,
  },
  distanceContainer: {
    flexDirection: "row",
    alignItems: "center",
    marginTop: 12,
    paddingTop: 8,
    borderTopWidth: 1,
    borderTopColor: "rgba(255, 255, 255, 0.1)",
  },
  distanceText: {
    color: "#00BFA6",
    fontSize: 14,
    fontWeight: "600",
    marginLeft: 6,
  },
  cardCentered: {
    backgroundColor: "rgba(255,255,255,0.05)",
    borderRadius: 16,
    padding: 24,
    borderWidth: 1,
    borderColor: "rgba(255,255,255,0.1)",
  },
});
