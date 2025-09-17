// Libraries Imports
import {
  View,
  Text,
  Image,
  StyleSheet,
  TouchableOpacity,
  Dimensions,
} from "react-native";
import { LinearGradient } from "expo-linear-gradient";
import { Ionicons } from "@expo/vector-icons";
import { useRef } from "react";
import * as Animatable from "react-native-animatable";
import { useRouter } from "expo-router";

const { width } = Dimensions.get("window");

export default function HomeScreen() {
  const router = useRouter();
  const viewRef = useRef(null);

  return (
    <View style={styles.container}>
      <Image
        source={{
          uri: "https://plus.unsplash.com/premium_photo-1676333345832-d2901e1b5a8c?w=800&auto=format&fit=crop&q=80",
        }}
        style={styles.background}
      />
      <LinearGradient
        colors={["rgba(0,0,0,0.9)", "rgba(0,0,0,0.7)", "rgba(0,0,0,0.4)"]}
        style={StyleSheet.absoluteFillObject}
      />
      <Animatable.View
        ref={viewRef}
        style={styles.content}
        animation="fadeInUp"
        duration={1500}
      >
        <View style={styles.glassCard}>
          <View style={styles.logoContainer}>
            <Image
              source={{
                uri: "https://plus.unsplash.com/premium_photo-1722873143746-232707ff0bb5?w=400&auto=format&fit=crop&q=80",
              }}
              style={{
                borderRadius: 60,
                height: 120,
                width: 120,
              }}
            />
          </View>
          <Text style={styles.title}>AI Dental Copilot</Text>
          <Text style={styles.subtitle}>
            Your intelligent assistant for dental health and care.
          </Text>

          <TouchableOpacity
            style={styles.button}
            onPress={() => router.navigate("./about")}
            activeOpacity={0.85}
          >
            <View style={styles.buttonSolid}>
              <Text style={styles.buttonText}>Get Started</Text>
              <Ionicons name="arrow-forward" size={22} color="#fff" />
            </View>
          </TouchableOpacity>
        </View>
      </Animatable.View>
    </View>
  );
}

// Styles
const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#000",
    justifyContent: "center",
    alignItems: "center",
  },
  background: {
    ...StyleSheet.absoluteFillObject,
    width: "100%",
    height: "100%",
  },
  content: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    padding: 20,
  },
  glassCard: {
    padding: 32,
    borderRadius: 28,
    alignItems: "center",
    backgroundColor: "rgba(255,255,255,0.08)",
    borderWidth: 1,
    borderColor: "rgba(255,255,255,0.15)",
    width: width * 0.88,
    shadowColor: "#000",
    shadowOffset: { width: 0, height: 12 },
    shadowOpacity: 0.35,
    shadowRadius: 12,
    elevation: 12,
    overflow: "hidden",
  },
  logoContainer: {
    width: 120,
    height: 120,
    borderRadius: 60,
    backgroundColor: "rgba(255,255,255,0.05)",
    justifyContent: "center",
    alignItems: "center",
    marginBottom: 25,
  },
  title: {
    fontSize: 34,
    fontWeight: "bold",
    color: "#ffffff",
    marginBottom: 14,
    textAlign: "center",
    letterSpacing: 1,
    fontFamily: "FunnelDisplay-Medium",
  },
  subtitle: {
    fontSize: 16,
    color: "rgba(255,255,255,0.85)",
    textAlign: "center",
    marginBottom: 42,
    lineHeight: 22,
    letterSpacing: 0.8,
    fontFamily: "FunnelDisplay-Medium",
  },
  button: {
    width: "100%",
    borderRadius: 22,
    overflow: "hidden",
  },
  buttonSolid: {
    backgroundColor: "#00BFA6",
    paddingVertical: 16,
    paddingHorizontal: 25,
    borderRadius: 22,
    flexDirection: "row",
    justifyContent: "center",
    alignItems: "center",
  },
  buttonText: {
    color: "#FFFFFF",
    fontSize: 18,
    fontWeight: "700",
    fontFamily: "FunnelDisplay-Medium",
    marginRight: 8,
  },
});
