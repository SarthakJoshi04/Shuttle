import { useState, useEffect } from "react";
import { AlertCircle, Loader2 } from "lucide-react";
import { Link, useNavigate } from "react-router-dom";

export default function Signup() {
  // Form state
  const [formData, setFormData] = useState({
    fullname: "",
    phoneNumber: "",
    location: "",
    password: "",
    confirmPassword: "",
  });

  // List of locations/cities for dropdown
  const [cities, setCities] = useState([]);

  // UI state
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const navigate = useNavigate();

  // Fetch available locations when component mounts
  useEffect(() => {
    fetch("http://localhost:8000/locations")
      .then((res) => res.json())
      .then((data) => setCities(data))
      .catch((err) => {
        console.error("Error fetching locations:", err);
        setError("Failed to load locations. Please refresh.");
      });
  }, []);

  // Update form state on input change
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  // Check if passwords match
  const passwordsMatch =
    formData.password &&
    formData.confirmPassword &&
    formData.password === formData.confirmPassword;

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setSuccess("");
    setIsLoading(true);

    if (!passwordsMatch) {
      setError("Passwords do not match");
      setIsLoading(false);
      return;
    }

    try {
      const response = await fetch("http://localhost:8000/register/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          fullname: formData.fullname,
          phone_number: formData.phoneNumber,
          password: formData.password,
          default_location: formData.location,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        setError(data.detail || "Registration failed");
        return;
      }

      setSuccess(data.message || "Registration successful");

      // Reset form after successful registration
      setFormData({
        fullname: "",
        phoneNumber: "",
        location: "",
        password: "",
        confirmPassword: "",
      });

      // Navigate to login page with success message
      navigate("/login", {
        state: {
          successMessage:
            data.message || "Account Registered. Login to continue.",
        },
      });
    } catch (err) {
      console.error("Registration error:", err);
      setError("Something went wrong! Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <main className="flex min-h-screen flex-col items-center justify-center bg-gray-50 py-12 px-4">
      <div className="w-full max-w-md bg-white shadow-lg rounded-xl p-6">
        {/* Header */}
        <h2 className="text-2xl font-bold text-center mb-2">
          Signup to Shuttle
        </h2>
        <p className="text-center text-gray-600 mb-6">
          Create your account by filling the information below
        </p>

        {/* Error Message */}
        {error && (
          <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-md flex items-start">
            <AlertCircle className="h-5 w-5 text-red-500 mr-2 flex-shrink-0 mt-0.5" />
            <p className="text-red-600 text-sm">{error}</p>
          </div>
        )}

        {/* Success Message */}
        {success && (
          <div className="mb-4 p-3 bg-green-50 border border-green-200 rounded-md flex items-start">
            <p className="text-green-600 text-sm">{success}</p>
          </div>
        )}

        {/* Signup Form */}
        <form onSubmit={handleSubmit} className="space-y-4">
          {/* Full Name */}
          <div>
            <label className="block text-sm font-medium text-gray-700">
              Full Name
            </label>
            <input
              type="text"
              name="fullname"
              placeholder="e.g. John Smith"
              value={formData.fullname}
              onChange={handleChange}
              required
              className="mt-1 block w-full rounded-lg border-gray-300 shadow-sm focus:border-teal-500 focus:ring-teal-500 sm:text-sm p-2 border"
            />
          </div>

          {/* Mobile Number */}
          <div>
            <label className="block text-sm font-medium text-gray-700">
              Mobile Number
            </label>
            <input
              type="tel"
              name="phoneNumber"
              placeholder="e.g. 9841321123"
              value={formData.phoneNumber}
              onChange={handleChange}
              required
              className="mt-1 block w-full rounded-lg border-gray-300 shadow-sm focus:border-teal-500 focus:ring-teal-500 sm:text-sm p-2 border"
            />
          </div>

          {/* Location */}
          <div>
            <label className="block text-sm font-medium text-gray-700">
              Location
            </label>
            <select
              name="location"
              value={formData.location}
              onChange={handleChange}
              required
              className="mt-1 block w-full rounded-lg border-gray-300 shadow-sm focus:border-teal-500 focus:ring-teal-500 sm:text-sm p-2 border"
            >
              <option value="" disabled>
                Select a location
              </option>
              {cities.map((city) => (
                <option key={city} value={city}>
                  {city}
                </option>
              ))}
            </select>
          </div>

          {/* Password */}
          <div>
            <label className="block text-sm font-medium text-gray-700">
              Password
            </label>
            <input
              type="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              required
              className="mt-1 block w-full rounded-lg border-gray-300 shadow-sm focus:border-teal-500 focus:ring-teal-500 sm:text-sm p-2 border"
            />
          </div>

          {/* Confirm Password */}
          <div>
            <label className="block text-sm font-medium text-gray-700">
              Confirm Password
            </label>
            <input
              type="password"
              name="confirmPassword"
              value={formData.confirmPassword}
              onChange={handleChange}
              required
              className="mt-1 block w-full rounded-lg border-gray-300 shadow-sm focus:border-teal-500 focus:ring-teal-500 sm:text-sm p-2 border"
            />
            {/* Password mismatch warning */}
            {!passwordsMatch && formData.confirmPassword && (
              <p className="text-xs text-red-500 mt-1">Passwords do not match</p>
            )}
          </div>

          {/* Submit Button */}
          <button
            type="submit"
            disabled={!passwordsMatch || isLoading}
            className="w-full flex justify-center items-center px-4 py-2 bg-teal-600 text-white rounded-lg shadow hover:bg-teal-700 disabled:opacity-70"
          >
            {isLoading ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Registering...
              </>
            ) : (
              "Sign Up"
            )}
          </button>
        </form>

        {/* Login Link */}
        <div className="text-center text-sm text-gray-600 mt-6">
          Already have an account?{" "}
          <Link to="/login" className="text-teal-600 hover:text-teal-700 font-medium">
            Login
          </Link>
        </div>
      </div>
    </main>
  );
}