// Libraries Imports
import * as Yup from "yup";
// Local Imports
import { DetailsFromTypes } from "@/types/details";

export const validationSchema: Yup.Schema<DetailsFromTypes> = Yup.object({
    name: Yup.string().min(3).required("Name is required!"),
    age: Yup.string().required("Age is required!"),
    gender: Yup.string().required("Gender is required!"),
    medical_history: Yup.string().default(""),
    additional_context: Yup.string().required(""),
    q1: Yup.string().required("This is required!"),
    q2: Yup.string().required("This is required!"),
    q3: Yup.string().required("This is required!"),
    q4: Yup.string().required("This is required!"),
    q5: Yup.string().required("This is required!"),
    file: Yup.string().required("Image is required!"),
});
