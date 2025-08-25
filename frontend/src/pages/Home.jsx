import { useState, useEffect, useContext } from "react";
import { Search, Car, ShoppingBag, AlertTriangle } from "lucide-react";
import { Link } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";
import ListingRow from "../components/ListingRow";

export default function Home() {
  const { user } = useContext(AuthContext); // Get logged-in user info
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedLocation, setSelectedLocation] = useState(
    user ? user.default_location : "Kathmandu"
  ); // Set default location if user is logged in or fallback
  const [locations, setLocations] = useState([]);
  const [recommendations, setRecommendations] = useState([]);
  const [loadingRecs, setLoadingRecs] = useState(false);
  const [recError, setRecError] = useState("");
  const [loadingLocations, setLoadingLocations] = useState(false);

  // Fetch locations from backend
  useEffect(() => {
    const fetchLocations = async () => {
      setLoadingLocations(true);
      try {
        const response = await fetch("http://localhost:8000/locations", {
          method: "GET",
          credentials: "include",
        });

        if (!response.ok) throw new Error("Failed to fetch locations");

        const data = await response.json();
        setLocations(data);
      } catch (err) {
        console.error("Error fetching locations:", err);
      } finally {
        setLoadingLocations(false);
      }
    };

    fetchLocations();
  }, []);

  // Update selected location when user changes
  useEffect(() => {
    if (user && user.default_location) {
      setSelectedLocation(user.default_location);
    }
  }, [user]);

  // Handle search submit
  const handleSearch = async (e) => {
    e.preventDefault();
    if (!searchQuery.trim()) return;

    setLoadingRecs(true);
    setRecError("");
    setRecommendations([]);

    try {
      const response = await fetch("http://localhost:8000/recommendations", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({
          query: searchQuery,
          location: selectedLocation,
        }),
      });

      if (!response.ok) {
        const text = await response.text();
        throw new Error(text || "Failed to fetch recommendations");
      }

      const data = await response.json();
      setRecommendations(data);
    } catch (error) {
      console.error("Error fetching recommendations:", error);
      setRecError("Could not fetch recommendations. Try again.");
    } finally {
      setLoadingRecs(false);
    }
  };

  // Update selected location from dropdown
  const handleLocationChange = (e) => {
    setSelectedLocation(e.target.value);
    // Clear current recommendations when location changes
    if (recommendations.length > 0) setRecommendations([]);
  };

  return (
    <main className="flex min-h-screen flex-col items-center">

      {/* Search Section */}
      <section className="w-full bg-gradient-to-r from-green-400 to-teal-500 py-20 px-4">
        <div className="max-w-6xl mx-auto text-center">
          <h1 className="text-4xl md:text-6xl font-bold text-white mb-6">
            Find Your Perfect Ride
          </h1>
          <p className="text-xl text-white mb-8">
            Rent or buy pre-owned vehicles directly from owners
          </p>

          {/* Search Form */}
          <form
            onSubmit={handleSearch}
            className="max-w-4xl mx-auto bg-white p-2 rounded-lg shadow-lg flex flex-col md:flex-row gap-2"
          >
            <input
              type="text"
              placeholder="Describe your ideal vehicle (e.g., 'a car for family trips')"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="flex-grow border-none focus:ring-0 focus:outline-none p-2 rounded"
            />

            {/* Location Dropdown */}
            <select
              value={selectedLocation}
              onChange={handleLocationChange}
              disabled={loadingLocations}
              className="px-4 py-2 border-none focus:ring-0 focus:outline-none rounded bg-gray-50 min-w-[150px]"
            >
              <option value="" disabled>Select Location</option>
              {loadingLocations ? (
                <option value="" disabled>Loading...</option>
              ) : (
                locations.map((location) => (
                  <option key={location} value={location}>
                    {location}
                  </option>
                ))
              )}
            </select>

            <button
              type="submit"
              className="px-6 py-2 bg-black text-white rounded hover:bg-black/70 flex items-center justify-center whitespace-nowrap"
            >
              <Search className="h-5 w-5 mr-2" />
              Find
            </button>
          </form>

          {/* Show selected location */}
          {selectedLocation && (
            <p className="text-white mt-4 opacity-90">
              Searching in: <span className="font-semibold">{selectedLocation}</span>
            </p>
          )}

          {/* Recommendations */}
          <div className="mt-10 w-full px-4">
            {loadingRecs && <p className="text-center py-4 text-white">Loading recommendations…</p>}
            {recError && <p className="text-center text-red-200 py-4">{recError}</p>}
            {!loadingRecs && !recError && recommendations.length === 0 && searchQuery.trim() !== "" && (
              <p className="text-center py-4 text-white opacity-90">
                No matching vehicles found in {selectedLocation}.
              </p>
            )}
            {!loadingRecs && recommendations.length > 0 && (
              <div className="space-y-6">
                <p className="text-white mb-4">
                  Found {recommendations.length} vehicle(s) in {selectedLocation}
                </p>
                {recommendations.map((listing) => (
                  <ListingRow key={listing.id} listing={listing} />
                ))}
              </div>
            )}
          </div>
        </div>
      </section>

      {/* Quick Links Section (Rentals, Marketplace, Report) */}
      <section className="w-full max-w-6xl mx-auto py-16 px-4 grid grid-cols-1 md:grid-cols-3 gap-8">
        <Link to="/rentals" className="group">
          <div className="bg-white rounded-lg shadow-md p-8 text-center transition-all duration-300 hover:shadow-xl">
            <div className="bg-green-100 p-4 rounded-full inline-flex mb-4 group-hover:bg-green-200 transition-colors">
              <Car className="h-8 w-8 text-green-600" />
            </div>
            <h2 className="text-2xl font-bold mb-4">Rentals</h2>
            <p className="text-gray-600">
              Browse vehicles available for short-term or long-term rental
            </p>
          </div>
        </Link>

        <Link to="/marketplace" className="group">
          <div className="bg-white rounded-lg shadow-md p-8 text-center transition-all duration-300 hover:shadow-xl">
            <div className="bg-blue-100 p-4 rounded-full inline-flex mb-4 group-hover:bg-blue-200 transition-colors">
              <ShoppingBag className="h-8 w-8 text-blue-600" />
            </div>
            <h2 className="text-2xl font-bold mb-4">Marketplace</h2>
            <p className="text-gray-600">
              Explore pre-owned vehicles for sale from verified owners
            </p>
          </div>
        </Link>

        <Link to="/report" className="group">
          <div className="bg-white rounded-lg shadow-md p-8 text-center transition-all duration-300 hover:shadow-xl">
            <div className="bg-red-100 p-4 rounded-full inline-flex mb-4 group-hover:bg-red-200 transition-colors">
              <AlertTriangle className="h-8 w-8 text-red-600" />
            </div>
            <h2 className="text-2xl font-bold mb-4">Report</h2>
            <p className="text-gray-600">
              Report stolen vehicles to help keep our community safe
            </p>
          </div>
        </Link>
      </section>

      {/* How Shuttle Works Section */}
      <section className="w-full bg-gray-50 py-16 px-4">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-3xl font-bold text-center mb-12">How Shuttle Works</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="text-center">
              
              <div className="bg-green-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl font-bold text-green-600">1</span>
              </div>
              <h3 className="text-xl font-semibold mb-2">Create an Account</h3>
              <p className="text-gray-600">Sign up and join our trusted community</p>
            </div>

            <div className="text-center">
              <div className="bg-green-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl font-bold text-green-600">2</span>
              </div>
              <h3 className="text-xl font-semibold mb-2">Browse or List</h3>
              <p className="text-gray-600">
                Find your perfect vehicle or list your own for rent or sale
              </p>
            </div>

            <div className="text-center">
              <div className="bg-green-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl font-bold text-green-600">3</span>
              </div>
              <h3 className="text-xl font-semibold mb-2">Connect Directly</h3>
              <p className="text-gray-600">
                Communicate with owners and arrange transactions securely
              </p>
            </div>
          </div>
        </div>
      </section>
    </main>
  );
}