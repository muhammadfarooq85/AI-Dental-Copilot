// Libraries Imports
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
// Local Imports
import { useColorScheme } from "@/hooks/use-color-scheme";

export default function RootLayout() {
  const colorScheme = useColorScheme();
  const [loaded, error] = useFonts({
    "FunnelDisplay-Medium": require("../assets/fonts/FunnelDisplay-Medium.ttf"),
  });
  console.log("error", error); // null
  console.log("loaded", loaded); // true

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
      <Stack>
        <Stack.Screen
          name="index"
          options={{
            headerShown: true,
            headerTitle: "Home",
            headerStyle: {
              backgroundColor: "#00BFA6",
            },
            headerTintColor: "#fff",
          }}
        />
        <Stack.Screen
          name="about"
          options={{
            headerShown: true,
            headerTitle: "About",
            headerStyle: {
              backgroundColor: "#00BFA6",
            },
            headerTintColor: "#fff",
          }}
        />
        <Stack.Screen
          name="details"
          options={{
            headerShown: true,
            headerTitle: "Details",
            headerStyle: {
              backgroundColor: "#00BFA6",
            },
            headerTintColor: "#fff",
          }}
        />
        <Stack.Screen
          name="report"
          options={{
            headerShown: true,
            headerTitle: "Report And Analysis",
            headerStyle: {
              backgroundColor: "#00BFA6",
            },
            headerTintColor: "#fff",
          }}
        />
      </Stack>
    </ThemeProvider>
  );
}
