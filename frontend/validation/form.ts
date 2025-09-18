import { FormValues } from "@/types/form";
import * as Yup from "yup";

export const validationSchema: Yup.Schema<FormValues> = Yup.object({
    q1: Yup.mixed<"Yes" | "No">()
        .oneOf(["Yes", "No"])
        .required("This is required!"),
    q2: Yup.mixed<"Yes" | "No">()
        .oneOf(["Yes", "No"])
        .required("This is required!"),
    q3: Yup.mixed<"Yes" | "No">()
        .oneOf(["Yes", "No"])
        .required("This is required!"),
    q4: Yup.mixed<"Yes" | "No">()
        .oneOf(["Yes", "No"])
        .required("This is required!"),
    q5: Yup.mixed<"Yes" | "No">()
        .oneOf(["Yes", "No"])
        .required("This is required!"),
    image: Yup.string().required("Image is required!"),
});
