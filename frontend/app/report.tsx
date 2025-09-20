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
import { useRouter, useLocalSearchParams } from "expo-router";
import { SafeAreaView } from "react-native-safe-area-context";

export default function ReportScreen() {
  const router = useRouter();
  const params = useLocalSearchParams();

  const analysisData = params.questionnaireResult
    ? JSON.parse(params.questionnaireResult as string)
    : null;
  const imageData = params.imageResult
    ? JSON.parse(params.imageResult as string)
    : null;

  if (!analysisData || !imageData) {
    return (
      <SafeAreaView style={styles.safeArea}>
        <View style={styles.cardCentered}>
          <Text style={styles.cardTitle}>⚠️ No Report Available</Text>
          <Text style={styles.cardText}>
            No report data found. Please try again.
          </Text>
        </View>
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView style={styles.safeArea} edges={["top", "bottom"]}>
      <ScrollView contentContainerStyle={styles.scrollContent}>
        <Animatable.View
          animation="fadeInDown"
          duration={1000}
          style={styles.header}
        >
          <Text style={styles.title}>Your Oral Health Report</Text>
          <View style={styles.divider} />
        </Animatable.View>
        <Animatable.View
          animation="fadeInUp"
          delay={100}
          duration={800}
          style={styles.card}
        >
          <Text style={styles.cardTitle}>AI Prediction</Text>
          <Text style={styles.cardText}>
            {imageData.prediction} {"\n"}
            Confidence: {(imageData.confidence * 100).toFixed(1)}%
          </Text>
          <Text style={styles.riskBadge}>
            Risk Level: {imageData.risk_level}
          </Text>
        </Animatable.View>
        <Animatable.View
          animation="fadeInUp"
          delay={300}
          duration={800}
          style={styles.card}
        >
          <Text style={styles.cardTitle}>Patient Questionnaire</Text>
          <Text style={styles.cardText}>{analysisData.summary_paragraph}</Text>
        </Animatable.View>
        <Animatable.View
          animation="fadeInUp"
          delay={500}
          duration={800}
          style={styles.card}
        >
          <Text style={styles.cardTitle}>Recommendations</Text>
          {imageData.recommendations.map((rec: string, i: number) => (
            <Text key={i} style={styles.listItem}>
              • {rec}
            </Text>
          ))}
          {analysisData.recommendations.map((rec: string, i: number) => (
            <Text key={`q-${i}`} style={styles.listItem}>
              • {rec}
            </Text>
          ))}
        </Animatable.View>
        <Animatable.View
          animation="fadeInUp"
          delay={700}
          duration={800}
          style={styles.card}
        >
          <Text style={styles.cardTitle}>Next Steps</Text>
          {analysisData.next_steps.map((step: string, i: number) => (
            <Text key={i} style={styles.listItem}>
              → {step}
            </Text>
          ))}
        </Animatable.View>
        <View style={styles.buttonRow}>
          <TouchableOpacity
            style={styles.button}
            onPress={() => router.navigate("/dentist")}
          >
            <Text style={styles.buttonText}>Find Dentists</Text>
            <Ionicons name="search" size={20} color="#fff" />
          </TouchableOpacity>
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
  scrollContent: {
    flexGrow: 1,
    padding: 20,
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
    backgroundColor: "#2563eb",
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
    fontFamily: "SpaceGrotesk-Medium",
  },
  cardText: {
    fontSize: 17,
    color: "rgba(255,255,255,0.8)",
    lineHeight: 22,
    marginBottom: 8,
    fontFamily: "SpaceGrotesk-Medium",
  },
  listItem: {
    fontSize: 17,
    color: "rgba(255,255,255,0.8)",
    marginBottom: 6,
    fontFamily: "SpaceGrotesk-Medium",
  },
  riskBadge: {
    marginTop: 10,
    padding: 8,
    backgroundColor: "#2563eb",
    color: "#ffffffff",
    borderRadius: 8,
    fontSize: 20,
    fontFamily: "SpaceGrotesk-Medium",
    textAlign: "center",
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
  cardCentered: {
    flex: 0.1,
    justifyContent: "center",
    alignItems: "center",
    backgroundColor: "rgba(255,255,255,0.05)",
    margin: 20,
    borderRadius: 16,
    padding: 24,
    borderWidth: 1,
    borderColor: "rgba(255,255,255,0.1)",
  },
});
