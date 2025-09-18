// Libraries Imports
import React from "react";
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  ScrollView,
} from "react-native";
import * as Animatable from "react-native-animatable";
import { Ionicons } from "@expo/vector-icons";
import { useRouter } from "expo-router";
// Local Imports
import { nearbyDoctors } from "../data/data";

export default function ReportScreen() {
  const reportSummary =
    "Based on the analysis of your oral health inputs, we’ve detected minor risk factors. We recommend consulting a dental professional for a detailed checkup.";

  const router = useRouter();

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Animatable.View
        animation="fadeInDown"
        duration={1000}
        style={styles.header}
      >
        <Text style={styles.title}>Your Report</Text>
        <View style={styles.divider} />
      </Animatable.View>
      <Animatable.View
        animation="fadeInUp"
        delay={200}
        duration={1000}
        style={styles.card}
      >
        <Text style={styles.cardTitle}>Summary</Text>
        <Text style={styles.cardText}>{reportSummary}</Text>
      </Animatable.View>
      <Animatable.View
        animation="fadeInUp"
        delay={600}
        duration={1000}
        style={styles.card}
      >
        <Text style={styles.cardTitle}>Nearby Dentists</Text>
        {nearbyDoctors.map((doc, index) => (
          <View key={index} style={styles.doctorBox}>
            <Ionicons name="person-circle" size={28} color="#00BFA6" />
            <View style={{ flex: 1, marginLeft: 10 }}>
              <Text style={styles.doctorName}>{doc.name}</Text>
              <View style={{ flexDirection: "row", alignItems: "center" }}>
                <Ionicons
                  name="location-outline"
                  size={14}
                  color="rgba(255,255,255,0.7)"
                />
                <Text style={styles.doctorAddress}>{doc.address}</Text>
              </View>
            </View>
          </View>
        ))}
      </Animatable.View>
      <Animatable.View
        animation="fadeInUp"
        delay={800}
        duration={1000}
        style={styles.buttonRow}
      >
        <TouchableOpacity
          style={[styles.button, styles.secondaryBtn]}
          onPress={() => router.navigate("/")}
        >
          <Ionicons name="home" size={20} color="#00BFA6" />
          <Text style={styles.secondaryText}>Go Home</Text>
        </TouchableOpacity>
        <TouchableOpacity
          style={styles.button}
          onPress={() => router.navigate("/details")}
        >
          <Text style={styles.buttonText}>Download</Text>
          <Ionicons name="download" size={20} color="#fff" />
        </TouchableOpacity>
      </Animatable.View>
    </ScrollView>
  );
}

// Styling
const styles = StyleSheet.create({
  container: {
    flexGrow: 1,
    padding: 20,
    backgroundColor: "#121212",
  },
  header: {
    alignItems: "center",
    marginBottom: 30,
  },
  title: {
    fontSize: 30,
    fontFamily: "SpaceGrotesk-Medium",
    color: "#fff",
    marginBottom: 12,
    textAlign: "center",
  },
  divider: {
    height: 3,
    width: 80,
    backgroundColor: "#00BFA6",
    borderRadius: 2,
  },
  card: {
    backgroundColor: "rgba(255,255,255,0.05)",
    borderRadius: 16,
    padding: 20,
    marginBottom: 20,
    borderWidth: 1,
    borderColor: "rgba(255,255,255,0.1)",
  },
  cardTitle: {
    fontSize: 25,
    color: "#fff",
    marginBottom: 12,
  },
  cardText: {
    fontSize: 17,
    color: "rgba(255,255,255,0.8)",
    lineHeight: 20,
    fontFamily: "SpaceGrotesk-Medium",
    letterSpacing: 0.5,
  },
  grid: {
    flexDirection: "row",
    flexWrap: "wrap",
    justifyContent: "space-between",
  },
  doctorBox: {
    flexDirection: "row",
    alignItems: "center",
    paddingVertical: 10,
    borderBottomWidth: 1,
    borderColor: "rgba(255,255,255,0.1)",
  },
  doctorName: {
    fontSize: 17,
    fontFamily: "SpaceGrotesk-Medium",
    color: "#fff",
    marginBottom: 2,
  },
  doctorAddress: {
    fontSize: 13,
    color: "rgba(255,255,255,0.8)",
    marginLeft: 4,
  },
  buttonRow: {
    flexDirection: "row",
    justifyContent: "space-between",
    marginTop: 10,
  },
  button: {
    flex: 1,
    backgroundColor: "#00BFA6",
    borderRadius: 20,
    paddingVertical: 14,
    flexDirection: "row",
    justifyContent: "center",
    alignItems: "center",
    marginHorizontal: 6,
  },
  buttonText: {
    color: "#fff",
    fontWeight: "600",
    fontSize: 25,
    fontFamily: "SpaceGrotesk-Medium",
    marginRight: 8,
  },
  secondaryBtn: {
    backgroundColor: "transparent",
    borderWidth: 1,
    borderColor: "#00BFA6",
  },
  secondaryText: {
    color: "#00BFA6",
    fontSize: 25,
    fontFamily: "SpaceGrotesk-Medium",
    marginLeft: 8,
  },
});
