import { useState, useEffect, useContext } from "react";
import { AlertCircle } from "lucide-react";
import { AuthContext } from "../context/AuthContext";

export default function ReportVehicle() {
  const { user } = useContext(AuthContext);
  const [vehicleTypes, setvehicleTypes] = useState([]);
  const [formData, setFormData] = useState({
    vehicleNo: "",
    vehicleType: "",
  });
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  useEffect(() => {
    fetch("http://localhost:8000/vehicle-types")
      .then((res) => res.json())
      .then((data) => setvehicleTypes(data))
      .catch((err) => {
        console.error("Error fetching vehicle types:", err);
        setError("Failed to load vehicle types. Please refresh.");
      });
  }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setSuccess("");

    if (!formData.vehicleNo || !formData.vehicleType) {
      setError("Please fill in all fields.");
      return;
    }

    if (!user?.id) {
      setError("You must be logged in to report a vehicle.");
      return;
    }

    setIsSubmitting(true);

     try {
      const body = new FormData();

      body.append("vehicle_no", formData.vehicleNo);
      body.append("vehicle_type", formData.vehicleType);

      const res = await fetch(
        `http://localhost:8000/vehicles/report/?user_id=${user.id}`,
        {
          method: "POST",
          body,
        }
      );

      if (!res.ok) {
        const data = await res.json();
        throw new Error(data.detail || "Failed to report vehicle");
      }

      const data = await res.json();
      setSuccess(data.message || "Vehicle reported successfully");

      // Reset form
      setFormData({ vehicleNo: "", vehicleType: "" });
    } catch (err) {
      setError(err.message);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <main className="flex-grow">
      {/* Header */}
      <section className="bg-gradient-to-r from-red-400 to-red-600 py-12 px-4">
        <div className="max-w-3xl mx-auto text-center">
          <h1 className="text-3xl md:text-4xl font-bold text-white mb-4">
            Report a Stolen Vehicle
          </h1>
          <p className="text-white text-lg">
            Help keep our community safe by reporting stolen vehicles
          </p>
        </div>
      </section>

      {/* Report Form */}
      <section className="flex-grow bg-gray-50 py-12 px-4">
        <div className="max-w-3xl mx-auto">
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h2 className="text-xl font-semibold mb-4">Vehicle Information</h2>
            <p className="text-gray-600 mb-6">
              Please provide as much detail as possible about the stolen vehicle
            </p>

            {error && (
              <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-md flex items-start">
                <AlertCircle className="h-5 w-5 text-red-500 mr-2 mt-0.5" />
                <p className="text-red-600 text-sm">{error}</p>
              </div>
            )}

            {success && (
              <div className="mb-4 p-3 bg-green-50 border border-green-200 rounded-md text-center">
                <p className="text-green-600 text-sm">{success}</p>
              </div>
            )}

            <form onSubmit={handleSubmit} className="space-y-4">
              {/* Vehicle No */}
              <div className="space-y-2">
                <label
                  htmlFor="vehicleNo"
                  className="block text-sm font-medium text-gray-700"
                >
                  Vehicle No.
                </label>
                <input
                  type="text"
                  id="vehicleNo"
                  name="vehicleNo"
                  placeholder="e.g. BA 1 PA 1234"
                  value={formData.vehicleNo}
                  onChange={handleChange}
                  required
                  className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-red-500"
                />
              </div>

              {/* Vehicle Type */}
              <div className="space-y-2">
                <label
                  htmlFor="vehicleType"
                  className="block text-sm font-medium text-gray-700"
                >
                  Vehicle Type
                </label>
                <select
                  id="vehicleType"
                  name="vehicleType"
                  value={formData.vehicleType}
                  onChange={handleChange}
                  required
                  className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-red-500"
                >
                  <option value="" disabled>Select a vehicle type</option>
                  {vehicleTypes.map((vehicleType) => (
                    <option key={vehicleType} value={vehicleType}>
                      {vehicleType}
                    </option>
                  ))}
                </select>
              </div>

              {/* Submit Button */}
              <div className="pt-2">
                <button
                  type="submit"
                  disabled={isSubmitting}
                  className="w-full bg-red-600 hover:bg-red-700 text-white font-medium py-2 px-4 rounded-md transition-colors disabled:opacity-70"
                >
                  {isSubmitting ? "Submitting..." : "Submit Report"}
                </button>
              </div>
            </form>
          </div>

          {/* Next Steps Section */}
          <div className="mt-8 bg-white p-6 rounded-lg shadow-md">
            <h2 className="text-xl font-semibold mb-4">What Happens Next?</h2>
            <ol className="space-y-3 list-decimal list-inside text-gray-700">
              <li>The vehicle will be added to our blacklist.</li>
              <li>Users will not be allowed to list the vehicle for rent or sale on Shuttle.</li>
            </ol>
          </div>
          <div className="mt-6 p-4 bg-yellow-50 border border-yellow-200 rounded-md">
              <p className="text-yellow-800 text-sm">
                <strong>Important:</strong> Please also file a police report for the stolen vehicle. This system is for preventing fraudulent listings only and doesn't replace official law enforcement procedures.
              </p>
            </div>
        </div>
      </section>
    </main>
  );
}