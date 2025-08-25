import { useState } from "react";
import { AuthContext } from "./AuthContext";
import { useNavigate } from "react-router-dom";

// ---------------------- AuthProvider Component ----------------------
export function AuthProvider({ children }) {
  // ---------------------- User State Initialization ----------------------
  // Load user from localStorage if available (persistent login)
  const [user, setUser] = useState(() => {
    const id = localStorage.getItem("user_id");
    const fullname = localStorage.getItem("fullname");
    const default_location = localStorage.getItem("default_location");
    return id ? { id, fullname, default_location } : null;
  });

  const navigate = useNavigate();

  // ---------------------- Login Function ----------------------
  const login = (userData) => {
    // Store user info in localStorage for persistence
    localStorage.setItem("user_id", userData.id);
    localStorage.setItem("fullname", userData.fullname);
    localStorage.setItem("default_location", userData.default_location);

    // Update React state
    setUser({
      id: userData.id,
      fullname: userData.fullname,
      default_location: userData.default_location,
    });
  };

  // ---------------------- Logout Function ----------------------
  const logout = async () => {
    try {
      // Send logout request to backend (to clear session cookies)
      await fetch("http://localhost:8000/logout/", {
        method: "POST",
        credentials: "include",
      });
    } catch (err) {
      console.error("Logout failed:", err);
    }

    // Remove user info from localStorage
    localStorage.removeItem("user_id");
    localStorage.removeItem("fullname");
    localStorage.removeItem("default_location");

    // Clear React state
    setUser(null);

    // Redirect to home page
    navigate("/");
  };

  // ---------------------- Context Provider ----------------------
  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children} {/* Render children components */}
    </AuthContext.Provider>
  );
}