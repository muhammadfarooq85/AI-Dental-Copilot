import { useFonts } from "expo-font";
import * as SplashScreen from "expo-splash-screen";
import { useEffect } from "react";
import {
  DarkTheme,
  DefaultTheme,
  ThemeProvider,
} from "@react-navigation/native";
import { Stack } from "expo-router";
import "react-native-reanimated";
import { StatusBar } from "expo-status-bar";

// Local Imports
import { useColorScheme } from "@/hooks/use-color-scheme";

export default function RootLayout() {
  const colorScheme = useColorScheme();
  const [loaded, error] = useFonts({
    "SpaceGrotesk-Medium": require("../assets/fonts/SpaceGrotesk-Medium.ttf"),
  });

  useEffect(() => {
    if (loaded || error) {
      SplashScreen.hideAsync();
    }
  }, [loaded, error]);

  if (!loaded && !error) {
    return null;
  }

  return (
    <ThemeProvider value={colorScheme === "dark" ? DarkTheme : DefaultTheme}>
      <StatusBar style="light" backgroundColor="#0d0d0d" />
      <Stack
        screenOptions={{
          headerShown: true,
          headerStyle: {
            backgroundColor: "#00BFA6",
          },
          headerTintColor: "#fff",
          headerTitleStyle: {
            fontFamily: "SpaceGrotesk-Medium",
            fontSize: 30,
            color: "#fff",
          },
        }}
      >
        <Stack.Screen name="index" options={{ headerTitle: "Home" }} />
        <Stack.Screen name="about" options={{ headerTitle: "About" }} />
        <Stack.Screen name="details" options={{ headerTitle: "Details" }} />
        <Stack.Screen
          name="report"
          options={{ headerTitle: "Report & Analysis" }}
        />
      </Stack>
    </ThemeProvider>
  );
}
