import axios from "axios";

export const apiClient = axios.create({
    baseURL: process.env.NEXT_PUBLIC_API_URL,
    headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
    },
});

export default apiClient;