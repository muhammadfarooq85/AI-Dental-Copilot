// Libraries Imports
import { useRouter } from "expo-router";
import {
  ScrollView,
  Text,
  View,
  StyleSheet,
  TouchableOpacity,
  Image,
} from "react-native";
import { Ionicons } from "@expo/vector-icons";
import * as Animatable from "react-native-animatable";
import { SafeAreaView } from "react-native-safe-area-context";
// Local Imports
import { howToUse, ourTechnology, teamMembers } from "../data/data";

export default function AboutScreen() {
  const router = useRouter();

  return (
    <SafeAreaView style={styles.safeArea} edges={["top", "bottom"]}>
      <ScrollView contentContainerStyle={styles.scrollContent}>
        <Animatable.View
          animation="fadeInDown"
          duration={900}
          style={styles.header}
        >
          <Text style={styles.title}>About AI Dental Copilot</Text>
          <View style={styles.divider} />
        </Animatable.View>
        <View style={styles.contentBox}>
          <Text style={styles.sectionTitle}>What We Do</Text>
          <Text style={styles.description}>
            AI Dental Copilot helps you monitor dental health using AI-driven
            image analysis, offering early insights so you can take better care
            of your smile.
          </Text>
        </View>
        <View style={styles.contentBox}>
          <Text style={styles.sectionTitle}>How To Use</Text>
          {howToUse.map((step) => (
            <View style={styles.stepContainer} key={step.num}>
              <View style={styles.stepNumber}>
                <Text style={styles.stepText}>{step.num}</Text>
              </View>
              <View style={styles.stepContent}>
                <Text style={styles.stepTitle}>{step.title}</Text>
              </View>
            </View>
          ))}
        </View>
        <View style={styles.contentBox}>
          <Text style={styles.sectionTitle}>Meet Our Team</Text>
          <ScrollView horizontal showsHorizontalScrollIndicator={false}>
            {teamMembers.map((member) => (
              <View key={member.id} style={styles.teamMember}>
                <Image source={{ uri: member.image }} style={styles.avatar} />
                <Text style={styles.memberName}>{member.name}</Text>
              </View>
            ))}
          </ScrollView>
        </View>
        <View style={styles.contentBox}>
          <Text style={styles.sectionTitle}>Our Technology</Text>
          <View style={styles.featureList}>
            {ourTechnology.map((feature, index) => (
              <View key={index} style={styles.featureItem}>
                <Ionicons name="checkmark-circle" size={20} color="#2563eb" />
                <Text style={styles.featureText}>{feature}</Text>
              </View>
            ))}
          </View>
        </View>
        <Animatable.View
          animation="fadeInUp"
          duration={1000}
          delay={600}
          style={styles.buttonContainer}
        >
          <TouchableOpacity
            style={styles.button}
            onPress={() => router.navigate("./details")}
            activeOpacity={0.85}
          >
            <Text style={styles.buttonText}>Fill Your Details</Text>
            <Ionicons name="document-text" size={22} color="#fff" />
          </TouchableOpacity>
        </Animatable.View>
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
    padding: 20,
  },
  header: {
    alignItems: "center",
    marginBottom: 28,
  },
  title: {
    fontSize: 30,
    color: "#fff",
    marginBottom: 12,
    textAlign: "center",
    fontFamily: "SpaceGrotesk-Medium",
  },
  divider: {
    height: 3,
    width: 70,
    backgroundColor: "#2563eb",
    borderRadius: 2,
  },
  contentBox: {
    backgroundColor: "rgba(255, 255, 255, 0.06)",
    borderRadius: 16,
    padding: 18,
    marginBottom: 22,
  },
  sectionTitle: {
    fontSize: 25,
    color: "#fff",
    marginBottom: 12,
    fontFamily: "SpaceGrotesk-Medium",
  },
  description: {
    fontFamily: "SpaceGrotesk-Medium",
    fontSize: 17,
    color: "rgba(255,255,255,0.8)",
    lineHeight: 20,
    letterSpacing: 0.5,
  },
  stepContainer: {
    flexDirection: "row",
    marginBottom: 18,
    alignItems: "flex-start",
  },
  stepNumber: {
    width: 30,
    height: 30,
    borderRadius: 15,
    backgroundColor: "#2563eb",
    justifyContent: "center",
    alignItems: "center",
    marginRight: 14,
  },
  stepText: {
    color: "#ffffffff",
    fontFamily: "SpaceGrotesk-Medium",
    fontSize: 15,
  },
  stepContent: {
    flex: 1,
  },
  stepTitle: {
    fontFamily: "SpaceGrotesk-Medium",
    fontSize: 17,
    color: "#ffffffe4",
    marginBottom: 4,
    letterSpacing: 0.5,
  },
  stepDescription: {
    fontSize: 15,
    color: "rgba(255,255,255,0.8)",
    lineHeight: 20,
    letterSpacing: 0.5,
  },
  teamMember: {
    width: 120,
    alignItems: "center",
    marginRight: 16,
    backgroundColor: "rgba(255,255,255,0.05)",
    borderRadius: 12,
    padding: 12,
  },
  avatar: {
    width: 70,
    height: 70,
    borderRadius: 35,
  },
  memberName: {
    fontSize: 15,
    fontFamily: "SpaceGrotesk-Medium",
    color: "#fff",
    textAlign: "center",
  },
  featureList: {
    marginTop: 12,
  },
  featureItem: {
    flexDirection: "row",
    alignItems: "center",
    marginBottom: 10,
  },
  featureText: {
    fontSize: 17,
    color: "rgba(255,255,255,0.85)",
    marginLeft: 8,
  },
  buttonContainer: {
    marginTop: 20,
  },
  button: {
    backgroundColor: "#2563eb",
    borderRadius: 20,
    paddingVertical: 14,
    flexDirection: "row",
    justifyContent: "center",
    alignItems: "center",
    elevation: 4,
  },
  buttonText: {
    color: "#fff",
    fontSize: 25,
    fontFamily: "SpaceGrotesk-Medium",
    marginRight: 8,
  },
});
