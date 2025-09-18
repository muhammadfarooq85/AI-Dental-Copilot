// Libraries Imports
import { View, Text, Image, StyleSheet, TouchableOpacity } from "react-native";
import { Ionicons } from "@expo/vector-icons";
import { useRouter } from "expo-router";

export default function HomeScreen() {
  const router = useRouter();

  return (
    <View style={styles.container}>
      <Image
        source={{
          uri: "https://plus.unsplash.com/premium_photo-1676333345832-d2901e1b5a8c?w=800&auto=format&fit=crop&q=80",
        }}
        style={styles.background}
      />
      <View style={styles.bottomCard}>
        <Text style={styles.title}>AI Dental Copilot</Text>
        <Text style={styles.subtitle}>
          Your intelligent assistant for dental health and care.
        </Text>
        <TouchableOpacity
          style={styles.button}
          onPress={() => router.push("./about")}
          activeOpacity={0.85}
        >
          <View style={styles.buttonSolid}>
            <Text style={styles.buttonText}>Get Started</Text>
            <Ionicons name="arrow-forward" size={22} color="#fff" />
          </View>
        </TouchableOpacity>
      </View>
    </View>
  );
}

// Styling
const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#111",
  },
  background: {
    ...StyleSheet.absoluteFillObject,
    width: "100%",
    height: "80%",
  },
  bottomCard: {
    position: "absolute",
    bottom: 0,
    width: "100%",
    height: "30%",
    backgroundColor: "#1A1A1A",
    padding: 24,
    borderTopLeftRadius: 28,
    borderTopRightRadius: 28,
    borderWidth: 1,
    borderColor: "rgba(255,255,255,0.08)",
    shadowColor: "#000",
    shadowOffset: { width: 0, height: -4 },
    shadowOpacity: 0.25,
    shadowRadius: 8,
    elevation: 8,
  },
  title: {
    fontSize: 30,
    color: "#fff",
    marginBottom: 10,
    textAlign: "center",
    letterSpacing: 1,
    fontFamily: "SpaceGrotesk-Medium",
  },
  subtitle: {
    fontSize: 20,
    color: "rgba(255,255,255,0.75)",
    textAlign: "center",
    marginBottom: 26,
    lineHeight: 22,
    fontFamily: "SpaceGrotesk-Medium",
  },
  button: {
    width: "100%",
    borderRadius: 20,
    overflow: "hidden",
  },
  buttonSolid: {
    backgroundColor: "#00BFA6",
    paddingVertical: 14,
    borderRadius: 20,
    flexDirection: "row",
    justifyContent: "center",
    alignItems: "center",
  },
  buttonText: {
    color: "#fff",
    marginRight: 8,
    fontSize: 25,
    fontFamily: "SpaceGrotesk-Medium",
  },
});
