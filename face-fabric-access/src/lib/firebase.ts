
import { initializeApp } from "firebase/app";
// import dotenv  from "dotenv";


// dotenv.config();
// import serviceaccount from "./firebase_service_account.json";

// Firebase configuration
// Note: In a production environment, these values should be stored in environment variables
const firebaseConfig = {
  apiKey: "AIzaSyDxwprf-4Oc1jg9EQopi0DBnnSUSeSZlSI",
  authDomain: "capst-222f4.firebaseapp.com",
  projectId: "capst-222f4",
  storageBucket: "capst-222f4.firebasestorage.app",
  messagingSenderId: "487121420613",
  appId: "1:487121420613:web:1d13b25de3d7029fa47e2c"
};

// Initialize Firebase
export const app = initializeApp(firebaseConfig);
