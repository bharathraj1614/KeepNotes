"use client";
import React, { useState } from "react";
import { useDispatch } from "react-redux";
import { loginUser } from "@/store/authSlice"; // Assuming you have this action
import { useRouter } from "next/navigation"; // Use next/navigation
import { useSearchParams } from "next/navigation";

export default function SignIn() {
  const dispatch = useDispatch();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const router = useRouter();

  const handleLogin = async (e) => {
    e.preventDefault();
    if (!email || !password) {
      setError("Please enter both email and password.");
      return;
    }
    try {
      const response = await fetch(`http://localhost:8000/token`, {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: new URLSearchParams({
          username: email,
          password: password,
        }),
      });

      const data = await response.json();

      if (response.ok) {
        // Store access token (example: localStorage)
        localStorage.setItem("accessToken", data.access_token);

        // Dispatch Redux action (if needed)
        dispatch(loginUser(data)); // Assuming loginUser handles token and user data

        // Redirect to home page
        router.push("/");
      } else {
        setError(data.detail || "Invalid credentials"); // Use the error message from the backend
      }
    } catch (err) {
      setError("Error during login");
      console.error(err);
    }
  };

  return (
    <div className="signin-container">
      <h1>Sign In</h1>
      {error && <p style={{ color: "red" }}>{error}</p>}
      <form onSubmit={handleLogin}>
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <button type="submit">Login</button>
      </form>
    </div>
  );
}
