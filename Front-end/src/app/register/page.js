"use client";
import React, { useState } from "react";
import { useDispatch } from "react-redux";
import { loginUser } from "@/store/authSlice"; // Assuming you have this action
import { useRouter } from "next/navigation"; // Use next/navigation
import { useSearchParams } from "next/navigation";

export default function SignUp() {
  const dispatch = useDispatch();
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    password: "",
    confirmPassword: "",
  });
  const [error, setError] = useState("");
  const router = useRouter();

  const handleChange = (e) =>
    setFormData({ ...formData, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (formData.password !== formData.confirmPassword) {
      setError("Passwords do not match");
      return;
    }
    try {
      const response = await fetch("http://localhost:8000/users", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          user_name: formData.name, // Adjust to match your backend's expected names
          user_email: formData.email,
          password: formData.password,
        }),
      });

      const data = await response.json();

      if (response.ok) {
        // Store access token (if received from signup)
        // localStorage.setItem('accessToken', data.access_token); // If your signup returns a token

        // Dispatch Redux action (if needed)
        dispatch(loginUser(data)); // Assuming loginUser handles user data

        // Redirect to home page
        router.push("/");
      } else {
        setError(data.detail || "Signup failed"); // Use the error message from the backend
      }
    } catch (err) {
      setError("Error during signup");
      console.error(err);
    }
  };

  return (
    <div className="signup-container">
      <h1>Sign Up</h1>
      {error && <p style={{ color: "red" }}>{error}</p>}
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          name="name"
          placeholder="Name"
          value={formData.name}
          onChange={handleChange}
          required
        />
        <input
          type="email"
          name="email"
          placeholder="Email"
          value={formData.email}
          onChange={handleChange}
          required
        />
        <input
          type="password"
          name="password"
          placeholder="Password"
          value={formData.password}
          onChange={handleChange}
          required
        />
        <input
          type="password"
          name="confirmPassword"
          placeholder="Confirm Password"
          value={formData.confirmPassword}
          onChange={handleChange}
          required
        />
        <button type="submit">Register</button>
      </form>
    </div>
  );
}
