import { useState, useEffect } from "react";
import { AuthContext } from "../context/AuthContext";

export default function Header({ title, subtitle }) {
  const user = AuthContext._currentValue.user; // Access user from AuthContext
  const [searchQuery, setSearchQuery] = useState("");
  const [locations, setLocations] = useState([]);
  const [selectedLocation, setSelectedLocation] = useState(user ? user.default_location : "Kathmandu");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");

  // Fetch locations from backend API on component mount
  useEffect(() => {
    const fetchLocations = async () => {
      setIsLoading(true);
      try {
        const response = await fetch("http://localhost:8000/locations", {
          method: "GET",
          credentials: "include", // Include session cookie for authentication, if required
        });

        if (!response.ok) {
          throw new Error("Failed to fetch locations");
        }

        const data = await response.json();
        setLocations(data); // Expecting an array of city names
      } catch (err) {
        setError("Failed to load locations. Please try again.");
        console.error("Error fetching locations:", err);
      } finally {
        setIsLoading(false);
      }
    };

    fetchLocations();
  }, []);

  // Handle search input change
  const handleSearchChange = (e) => {
    setSearchQuery(e.target.value);
  };

  // Handle location selection change
  const handleLocationChange = (e) => {
    setSelectedLocation(e.target.value);
  };

  return (
    <>
      {/* Header */}
      <section className="bg-gradient-to-r from-green-400 to-teal-500 py-12 px-4">
        <div className="max-w-6xl mx-auto">
          <h1 className="text-3xl md:text-4xl font-bold text-white mb-4">
            {title}
          </h1>
          <p className="text-white text-lg">{subtitle}</p>
        </div>
      </section>

      {/* Filters and Search */}
      <section className="bg-white shadow-md py-6 px-4 sticky top-0 z-10">
        <div className="max-w-6xl mx-auto flex flex-col md:flex-row gap-4">
          <div className="flex-grow">
            <input
              type="text"
              placeholder="Search vehicles..."
              value={searchQuery}
              onChange={handleSearchChange}
              className="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-teal-500"
            />
          </div>

          <div className="flex flex-wrap gap-2">
            <select
              value={selectedLocation}
              onChange={handleLocationChange}
              disabled={isLoading || error}
              className="px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-teal-500 w-max"
            >
              <option value="" disabled>Select Location</option>
              {isLoading ? (
                <option value="" disabled>
                  Loading...
                </option>
              ) : error ? (
                <option value="" disabled>
                  Error loading locations
                </option>
              ) : (
                locations.map((location) => (
                  <option key={location} value={location}>
                    {location}
                  </option>
                ))
              )}
            </select>
          </div>
        </div>
      </section>
    </>
  );
}