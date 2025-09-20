import * as Yup from "yup";

export const dentistValidationSchema = Yup.object().shape({
    address: Yup.string().required("Address is required"),
    city: Yup.string().required("City is required"),
    state: Yup.string().required("State is required"),
    country: Yup.string().required("Country is required"),
    radius_km: Yup.number()
        .typeError("Radius must be a number")
        .positive("Radius must be greater than 0")
        .required("Radius is required"),
});
