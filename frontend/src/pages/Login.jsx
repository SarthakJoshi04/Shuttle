import { useState, useEffect, useContext } from "react";
import { AlertCircle, Loader2 } from "lucide-react";
import { Link, useNavigate, useLocation } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";

export default function LoginPage() {
  // Form state for phone number and password
  const [formData, setFormData] = useState({ phone_number: "", password: "" });
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const navigate = useNavigate();
  const location = useLocation(); // Get current location (to read success messages from redirects)
  const { login } = useContext(AuthContext); // Auth context to update user login state

  // Display success message after coming from Signup page after successful registration
  useEffect(() => {
    if (location.state?.successMessage) {
      setSuccess(location.state.successMessage);
      // Clear history state so message doesn't persist on refresh
      window.history.replaceState({}, document.title);
    }
  }, [location.state]);

  // Handle input changes
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError("");
    setSuccess("");

    // Simple client-side validation
    if (!formData.phone_number || !formData.password) {
      setError("Please enter both phone number and password");
      setIsLoading(false);
      return;
    }

    try {
      // Make login request to backend
      const response = await fetch("http://localhost:8000/login/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
        credentials: "include", // Include session cookie for authentication
      });

      const data = await response.json();

      if (!response.ok) {
        setError(data.detail || "Login failed");
        return;
      }

      setSuccess("Login successful");

      // Update AuthContext with user info (automatically updates Navbar)
      login({
        id: data.id,
        fullname: data.fullname,
        default_location: data.default_location,
      });

      // Redirect to home page after 1 second delay
      setTimeout(() => navigate("/"), 1000);
    } catch (err) {
      console.error("Login error:", err);
      setError("Something went wrong! Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <main className="flex min-h-screen flex-col items-center justify-center bg-gray-50 py-12 px-4">
      <div className="w-full max-w-md bg-white shadow-lg rounded-xl p-6">
        {/* Header */}
        <h2 className="text-2xl font-bold text-center mb-2">Login to Shuttle</h2>
        <p className="text-center text-gray-600 mb-6">
          Enter your credentials to access your account
        </p>

        {/* Display error messages */}
        {error && (
          <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-md flex items-start">
            <AlertCircle className="h-5 w-5 text-red-500 mr-2 flex-shrink-0 mt-0.5" />
            <p className="text-red-600 text-sm">{error}</p>
          </div>
        )}

        {/* Display success messages */}
        {success && (
          <div className="mb-4 p-3 bg-green-50 border border-green-200 rounded-md flex items-start">
            <p className="text-green-600 text-sm">{success}</p>
          </div>
        )}

        {/* Login form */}
        <form onSubmit={handleSubmit} className="space-y-4">
          {/* Phone Number Input */}
          <div>
            <label htmlFor="phone_number" className="block text-sm font-medium text-gray-700">
              Phone Number
            </label>
            <input
              id="phone_number"
              name="phone_number"
              type="tel"
              placeholder="98XXXXXXXX"
              value={formData.phone_number}
              onChange={handleChange}
              required
              className="mt-1 block w-full rounded-lg border-gray-300 shadow-sm focus:border-teal-500 focus:ring-teal-500 sm:text-sm p-2 border"
            />
          </div>

          {/* Password Input */}
          <div>
            <label htmlFor="password" className="block text-sm font-medium text-gray-700">
              Password
            </label>
            <input
              id="password"
              name="password"
              type="password"
              value={formData.password}
              onChange={handleChange}
              required
              className="mt-1 block w-full rounded-lg border-gray-300 shadow-sm focus:border-teal-500 focus:ring-teal-500 sm:text-sm p-2 border"
            />
          </div>

          {/* Submit Button */}
          <button
            type="submit"
            className="w-full flex justify-center items-center px-4 py-2 bg-teal-600 text-white rounded-lg shadow hover:bg-teal-700 disabled:opacity-70"
            disabled={isLoading}
          >
            {isLoading ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Logging in...
              </>
            ) : (
              "Login"
            )}
          </button>
        </form>

        {/* Signup link */}
        <div className="text-center text-sm text-gray-600 mt-6">
          Don&apos;t have an account?{" "}
          <Link to="/signup" className="text-teal-600 hover:text-teal-700 font-medium">
            Signup
          </Link>
        </div>
      </div>
    </main>
  );
}