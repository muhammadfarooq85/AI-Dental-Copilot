// Libraries Imorts
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
// Local Imports
import { howToUse, ourTechnology, teamMembers } from "../data/data";

export default function AboutScreen() {
  const router = useRouter();

  return (
    <View style={styles.container}>
      <ScrollView contentContainerStyle={styles.scrollContent}>
        <Animatable.View
          animation="fadeInDown"
          duration={1000}
          style={styles.header}
        >
          <Text style={styles.title}>About AI Dental Copilot</Text>
          <View style={styles.divider} />
        </Animatable.View>
        <Animatable.View
          animation="fadeInUp"
          duration={1000}
          delay={300}
          style={styles.contentBox}
        >
          <Text style={styles.sectionTitle}>What We Do</Text>
          <Text style={styles.description}>
            AI Dental Copilot is an innovative application that uses artificial
            intelligence to help you monitor your dental health. Our advanced
            algorithms can analyze dental images and provide insights about
            potential issues, helping you take better care of your smile.
          </Text>
        </Animatable.View>

        {/* How To Use */}
        <Animatable.View
          animation="fadeInUp"
          duration={1000}
          delay={500}
          style={styles.contentBox}
        >
          <Text style={styles.sectionTitle}>How To Use</Text>
          {howToUse.map((step) => (
            <View style={styles.stepContainer} key={step.num}>
              <View style={styles.stepNumber}>
                <Text style={styles.stepText}>{step.num}</Text>
              </View>
              <View style={styles.stepContent}>
                <Text style={styles.stepTitle}>{step.title}</Text>
                <Text style={styles.stepDescription}>{step.desc}</Text>
              </View>
            </View>
          ))}
        </Animatable.View>
        <Animatable.View
          animation="fadeInUp"
          duration={1000}
          delay={700}
          style={styles.contentBox}
        >
          <Text style={styles.sectionTitle}>Meet Our Team</Text>
          <Text style={styles.description}>
            Our dedicated team of professionals combines expertise in dentistry,
            artificial intelligence, and user experience to deliver the best
            dental health solutions.
          </Text>

          <View style={styles.teamGrid}>
            {teamMembers.map((member) => (
              <View key={member.id} style={styles.teamMember}>
                <Image source={{ uri: member.image }} style={styles.avatar} />
                <Text style={styles.memberName}>{member.name}</Text>
                <Text style={styles.memberRole}>{member.role}</Text>
              </View>
            ))}
          </View>
        </Animatable.View>
        <Animatable.View
          animation="fadeInUp"
          duration={1000}
          delay={900}
          style={styles.contentBox}
        >
          <Text style={styles.sectionTitle}>Our Technology</Text>
          <Text style={styles.description}>
            Using cutting-edge machine learning algorithms trained on thousands
            of dental images, our AI provides accurate preliminary assessments
            to help you understand your dental health better.
          </Text>

          <View style={styles.featureList}>
            {ourTechnology.map((feature, index) => (
              <View key={index} style={styles.featureItem}>
                <Ionicons name="checkmark-circle" size={20} color="#00BFA6" />
                <Text style={styles.featureText}>{feature}</Text>
              </View>
            ))}
          </View>
        </Animatable.View>
      </ScrollView>
      <Animatable.View
        animation="fadeInUp"
        duration={1000}
        delay={1100}
        style={styles.buttonContainer}
      >
        <TouchableOpacity
          style={styles.button}
          onPress={() => router.navigate("./details")}
          activeOpacity={0.85}
        >
          <Ionicons name="document-text" size={22} color="#fff" />
          <Text style={styles.buttonText}>Fill Your Details</Text>
        </TouchableOpacity>
      </Animatable.View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#0d0d0d",
  },
  scrollContent: {
    padding: 24,
    paddingBottom: 120,
  },
  header: {
    alignItems: "center",
    marginBottom: 36,
    marginTop: 24,
  },
  title: {
    fontSize: 30,
    fontWeight: "800",
    color: "#ffffff",
    marginBottom: 18,
    textAlign: "center",
    letterSpacing: 0.5,
  },
  divider: {
    height: 3,
    width: 80,
    backgroundColor: "#00BFA6",
    borderRadius: 2,
  },
  contentBox: {
    backgroundColor: "rgba(255, 255, 255, 0.08)",
    borderRadius: 18,
    padding: 22,
    marginBottom: 28,
    borderWidth: 1,
    borderColor: "rgba(255, 255, 255, 0.1)",
  },
  sectionTitle: {
    fontSize: 22,
    fontWeight: "700",
    color: "#ffffff",
    marginBottom: 14,
  },
  description: {
    fontSize: 16,
    color: "rgba(255, 255, 255, 0.85)",
    lineHeight: 24,
    marginBottom: 12,
  },
  stepContainer: {
    flexDirection: "row",
    marginBottom: 22,
    alignItems: "flex-start",
  },
  stepNumber: {
    width: 34,
    height: 34,
    borderRadius: 17,
    backgroundColor: "rgba(0, 191, 166, 0.18)",
    justifyContent: "center",
    alignItems: "center",
    marginRight: 16,
    marginTop: 2,
  },
  stepText: {
    color: "#00BFA6",
    fontWeight: "700",
    fontSize: 16,
  },
  stepContent: {
    flex: 1,
  },
  stepTitle: {
    fontSize: 18,
    fontWeight: "600",
    color: "#ffffff",
    marginBottom: 6,
  },
  stepDescription: {
    fontSize: 14,
    color: "rgba(255, 255, 255, 0.7)",
    lineHeight: 21,
  },
  teamGrid: {
    flexDirection: "row",
    flexWrap: "wrap",
    justifyContent: "space-between",
    marginTop: 18,
  },
  teamMember: {
    width: "47%",
    alignItems: "center",
    marginBottom: 22,
    backgroundColor: "rgba(255, 255, 255, 0.06)",
    borderRadius: 14,
    padding: 14,
  },
  avatar: {
    width: 84,
    height: 84,
    borderRadius: 42,
    marginBottom: 12,
  },
  memberName: {
    fontSize: 16,
    fontWeight: "600",
    color: "#ffffff",
    textAlign: "center",
    marginBottom: 4,
  },
  memberRole: {
    fontSize: 13,
    color: "rgba(255, 255, 255, 0.7)",
    textAlign: "center",
  },
  featureList: {
    marginTop: 18,
  },
  featureItem: {
    flexDirection: "row",
    alignItems: "center",
    marginBottom: 12,
  },
  featureText: {
    fontSize: 15,
    color: "rgba(255, 255, 255, 0.85)",
    marginLeft: 10,
  },
  buttonContainer: {
    position: "absolute",
    bottom: 30,
    left: 20,
    right: 20,
  },
  button: {
    backgroundColor: "#00BFA6",
    borderRadius: 24,
    paddingVertical: 16,
    flexDirection: "row",
    justifyContent: "center",
    alignItems: "center",
    elevation: 6,
  },
  buttonText: {
    color: "#ffffff",
    fontSize: 18,
    fontWeight: "700",
    letterSpacing: 0.4,
    marginLeft: 8,
  },
});
