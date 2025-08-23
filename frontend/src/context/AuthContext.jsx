import { useState } from "react";
import { AuthContext } from "./AuthContext";
import { useNavigate } from "react-router-dom";

export function AuthProvider({ children }) {
  const [user, setUser] = useState(() => {
    const id = localStorage.getItem("user_id");
    const fullname = localStorage.getItem("fullname");
    const default_location = localStorage.getItem("default_location");
    return id ? { id, fullname, default_location } : null;
  });

  const navigate = useNavigate();

  const login = (userData) => {
    localStorage.setItem("user_id", userData.id);
    localStorage.setItem("fullname", userData.fullname);
    localStorage.setItem("default_location", userData.default_location);
    setUser({
      id: userData.id,
      fullname: userData.fullname,
      default_location: userData.default_location
    });
  };

  const logout = async () => {
    try {
      await fetch("http://localhost:8000/logout/", {
        method: "POST",
        credentials: "include",
      });
    } catch (err) {
      console.error("Logout failed:", err);
    }
    localStorage.removeItem("user_id");
    localStorage.removeItem("fullname");
    localStorage.removeItem("default_location");
    setUser(null);

    navigate("/");
  };

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}