import { useState, useEffect, useContext } from "react";
import { AlertCircle, Loader2 } from "lucide-react";
import { AuthContext } from "../context/AuthContext";

export default function ListVehicle() {
  // Get logged-in user from context
  const { user } = useContext(AuthContext);
  const userId = user?.id;

  // State for vehicle-related fields
  const [vehicleData, setVehicleData] = useState({
    vehicle_no: "",
    vehicle_type: "",
    engine_type: "",
    engine_battery_capacity: "",
    body_type: "",
    company: "",
    model_name: "",
  });

  // State for listing-related fields
  const [listingData, setListingData] = useState({
    title: "",
    description: "",
    listing_type: "",
    price: "",
    location: "",
  });

  // Dropdown options for selects
  const [dropdowns, setDropdowns] = useState({
    cities: [],
    vehicleTypes: [],
    engineTypes: [],
    listingTypes: [],
    carBodyTypes: [],
    bikeBodyTypes: [],
  });

  const [isLoading, setIsLoading] = useState(true);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [image, setImage] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);

  // Fetch dropdown options from backend
  useEffect(() => {
    const fetchDropdowns = async () => {
      try {
        const [citiesRes, vehicleTypesRes, engineTypesRes, listingTypesRes, carBodyRes, bikeBodyRes] = await Promise.all([
          fetch("http://localhost:8000/locations").then((r) => r.json()),
          fetch("http://localhost:8000/vehicle-types").then((r) => r.json()),
          fetch("http://localhost:8000/engine-types").then((r) => r.json()),
          fetch("http://localhost:8000/listing-types").then((r) => r.json()),
          fetch("http://localhost:8000/car-body-types").then((r) => r.json()),
          fetch("http://localhost:8000/bike-body-types").then((r) => r.json()),
        ]);

        setDropdowns({
          cities: citiesRes,
          vehicleTypes: vehicleTypesRes,
          engineTypes: engineTypesRes,
          listingTypes: listingTypesRes,
          carBodyTypes: carBodyRes,
          bikeBodyTypes: bikeBodyRes,
        });
      } catch (err) {
        console.error("Failed to fetch dropdowns:", err);
        setError("Failed to load dropdown values. Please refresh.");
      } finally {
        setIsLoading(false);
      }
    };

    fetchDropdowns();
  }, []);

  // Update vehicle data state on input change
  const handleVehicleChange = (e) => {
    const { name, value } = e.target;
    setVehicleData((prev) => ({
      ...prev,
      [name]: value,
      // Reset body_type if vehicle_type changes
      ...(name === "vehicle_type" ? { body_type: "" } : {}),
    }));
  };

  // Update listing data state on input change
  const handleListingChange = (e) => {
    const { name, value } = e.target;
    setListingData((prev) => ({ ...prev, [name]: value }));
  };

  // Handle image file selection
  const handleImageChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      // Validate file type
      const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp'];
      if (!allowedTypes.includes(file.type)) {
        setError("Invalid file type. Please upload a JPEG, PNG, GIF, or WebP image.");
        return;
      }

      // Validate file size (max 5MB)
      const maxSize = 5 * 1024 * 1024; // 5MB
      if (file.size > maxSize) {
        setError("File too large. Please upload an image smaller than 5MB.");
        return;
      }

      setImage(file);

      // Create preview
      const reader = new FileReader();
      reader.onloadend = () => {
        setImagePreview(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log("Form submitted, userId:", userId);
    setError("");
    setSuccess("");

    if (!userId) {
      setError("You must be logged in to list a vehicle.");
      return;
    }

    // Validate all required fields
    const requiredFields = [
      'vehicle_no', 'vehicle_type', 'engine_type', 'engine_battery_capacity',
      'body_type', 'company', 'model_name', 'title', 'listing_type', 'price', 'location'
    ];
    
    const missingFields = requiredFields.filter(field => {
      const value = vehicleData[field] || listingData[field];
      return !value || value === "";
    });
    
    if (missingFields.length > 0) {
      setError(`Please fill in all required fields: ${missingFields.join(', ')}`);
      return;
    }

    if (!image) {
      setError("Please upload a vehicle image.");
      return;
    }

    setIsSubmitting(true);

    try {
      // Create FormData for multipart/form-data upload
      const formData = new FormData();
      
      // Add vehicle data
      formData.append('vehicle_no', vehicleData.vehicle_no);
      formData.append('vehicle_type', vehicleData.vehicle_type);
      formData.append('engine_type', vehicleData.engine_type);
      formData.append('engine_battery_capacity', vehicleData.engine_battery_capacity);
      formData.append('body_type', vehicleData.body_type);
      formData.append('company', vehicleData.company);
      formData.append('model_name', vehicleData.model_name);
      
      // Add listing data
      formData.append('title', listingData.title);
      formData.append('description', listingData.description);
      formData.append('listing_type', listingData.listing_type);
      formData.append('price', listingData.price);
      formData.append('location', listingData.location);
      
      // Add image file
      formData.append('image', image);

      const res = await fetch(`http://localhost:8000/vehicles/list/?user_id=${encodeURIComponent(userId)}`, {
        method: "POST",
        credentials: "include",
        body: formData, // Don't set Content-Type header, let browser set it
      });

      const data = await res.json();

      if (!res.ok) {
        // Handle validation errors from FastAPI
        if (data.detail && Array.isArray(data.detail)) {
          const errorMessages = data.detail.map(err => `${err.loc.join('.')}: ${err.msg}`);
          setError(errorMessages.join(', '));
        } else {
          setError(data.detail || "Failed to list vehicle.");
        }
      } else {
        setSuccess("Vehicle listed successfully!");

        // Reset form
        setVehicleData({
          vehicle_no: "",
          vehicle_type: "",
          engine_type: "",
          engine_battery_capacity: "",
          body_type: "",
          company: "",
          model_name: "",
        });
        setListingData({
          title: "",
          description: "",
          listing_type: "",
          price: "",
          location: "",
        });
        setImage(null);
        setImagePreview(null);
        
        // Reset file input
        const fileInput = document.querySelector('input[type="file"]');
        if (fileInput) {
          fileInput.value = '';
        }
      }
    } catch (err) {
      console.error(err);
      setError("Something went wrong! Please try again.");
    } finally {
      setIsSubmitting(false);
    }
  };

  if (isLoading) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <Loader2 className="animate-spin h-8 w-8 text-teal-600" />
      </div>
    );
  }

  const bodyTypes =
    vehicleData.vehicle_type?.toLowerCase() === "car"
      ? dropdowns.carBodyTypes
      : vehicleData.vehicle_type?.toLowerCase() === "bike"
      ? dropdowns.bikeBodyTypes
      : [];

  return (
    <main className="flex min-h-screen flex-col items-center justify-center bg-gray-50 py-12 px-4">
      <div className="w-full max-w-3xl bg-white shadow-lg rounded-xl p-6">
        <h1 className="text-2xl font-bold text-center mb-4">List Your Vehicle</h1>

        {error && (
          <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-md flex items-start">
            <AlertCircle className="h-5 w-5 text-red-500 mr-2 mt-0.5" />
            <p className="text-red-600 text-sm">{error}</p>
          </div>
        )}

        {success && (
          <div className="mb-4 p-3 bg-green-50 border border-green-200 rounded-md">
            <p className="text-green-600 text-sm">{success}</p>
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          {/* Listing Title */}
          <div>
            <label className="block text-sm font-medium text-gray-700">Listing Title</label>
            <input
              type="text"
              name="title"
              placeholder="e.g. Honda Hornet 2.0 for Rent"
              value={listingData.title}
              onChange={handleListingChange}
              className="mt-1 block w-full rounded-lg border-gray-300 shadow-sm p-2"
              required
            />
          </div>

          {/* Vehicle Image */}
          <div>
            <label className="block text-sm font-medium text-gray-700">Upload Image</label>
            <input
              type="file"
              name="image"
              accept="image/*"
              onChange={handleImageChange}
              className="mt-1 block w-full text-sm text-gray-500
                        file:mr-4 file:py-2 file:px-4
                        file:rounded-lg file:border-0
                        file:text-sm file:font-semibold
                        file:bg-blue-50 file:text-blue-700
                        hover:file:bg-blue-100"
              required
            />
            <p className="mt-1 text-xs text-gray-500">Upload a clear photo of your vehicle (Max 5MB)</p>
            
            {/* Image Preview */}
            {imagePreview && (
              <div className="mt-3">
                <img
                  src={imagePreview}
                  alt="Vehicle preview"
                  className="max-w-xs max-h-48 rounded-lg border border-gray-300 object-cover"
                />
              </div>
            )}
          </div>

          {/* Listing Type */}
          <div>
            <label className="block text-sm font-medium text-gray-700">Listing Type</label>
            <select
              name="listing_type"
              value={listingData.listing_type}
              onChange={handleListingChange}
              className="mt-1 block w-full rounded-lg border-gray-300 shadow-sm p-2"
              required
            >
              <option value="" disabled>Select Listing Type</option>
              {dropdowns.listingTypes.map((type) => (
                <option key={type} value={type}>
                  {type}
                </option>
              ))}
            </select>
          </div>

          {/* Price */}
          <div>
            <label className="block text-sm font-medium text-gray-700">Price (NRs.)</label>
            <p className="text-xs mt-1 text-gray-500">Enter the hourly rate for rentals or the total price for sales.</p>
            <input
              type="number"
              name="price"
              tooltip="Hourly for Rent, Total for Sale"
              placeholder="e.g. 1500"
              value={listingData.price}
              onChange={handleListingChange}
              className="mt-1 block w-full rounded-lg border-gray-300 shadow-sm p-2"
              required
            />
          </div>

          {/* Location */}
          <div>
            <label className="block text-sm font-medium text-gray-700">Location</label>
            <select
              name="location"
              value={listingData.location}
              onChange={handleListingChange}
              className="mt-1 block w-full rounded-lg border-gray-300 shadow-sm p-2"
              required
            >
              <option value="" disabled>Select City</option>
              {dropdowns.cities.map((city) => (
                <option key={city} value={city}>
                  {city}
                </option>
              ))}
            </select>
          </div>

          {/* Company */}
          <div>
            <label className="block text-sm font-medium text-gray-700">Company</label>
            <input
              type="text"
              name="company"
              placeholder="e.g. Honda"
              value={vehicleData.company}
              onChange={handleVehicleChange}
              className="mt-1 block w-full rounded-lg border-gray-300 shadow-sm p-2"
              required
            />
          </div>

          {/* Model Name */}
          <div>
            <label className="block text-sm font-medium text-gray-700">Model Name</label>
            <input
              type="text"
              name="model_name"
              placeholder="e.g. Hornet 2.0"
              value={vehicleData.model_name}
              onChange={handleVehicleChange}
              className="mt-1 block w-full rounded-lg border-gray-300 shadow-sm p-2"
              required
            />
          </div>

          {/* Vehicle Number */}
          <div>
            <label className="block text-sm font-medium text-gray-700">Vehicle Number</label>
            <input
              type="text"
              name="vehicle_no"
              placeholder="e.g. BA 1 PA 1234"
              value={vehicleData.vehicle_no}
              onChange={handleVehicleChange}
              className="mt-1 block w-full rounded-lg border-gray-300 shadow-sm p-2"
              required
            />
          </div>

          {/* Vehicle Type */}
          <div>
            <label className="block text-sm font-medium text-gray-700">Vehicle Type</label>
            <select
              name="vehicle_type"
              value={vehicleData.vehicle_type}
              onChange={handleVehicleChange}
              className="mt-1 block w-full rounded-lg border-gray-300 shadow-sm p-2"
              required
            >
              <option value="" disabled>Select Vehicle Type</option>
              {dropdowns.vehicleTypes.map((type) => (
                <option key={type} value={type}>
                  {type}
                </option>
              ))}
            </select>
          </div>

          {/* Body Type */}
          <div>
            <label className="block text-sm font-medium text-gray-700">Body Type</label>
            <select
              name="body_type"
              value={vehicleData.body_type}
              onChange={handleVehicleChange}
              className="mt-1 block w-full rounded-lg border-gray-300 shadow-sm p-2"
              required
              disabled={!bodyTypes.length}
            >
              <option value="" disabled>Select Body Type</option>
              {bodyTypes.map((type) => (
                <option key={type} value={type}>
                  {type}
                </option>
              ))}
            </select>
          </div>

          {/* Engine Type */}
          <div>
            <label className="block text-sm font-medium text-gray-700">Engine Type</label>
            <select
              name="engine_type"
              value={vehicleData.engine_type}
              onChange={handleVehicleChange}
              className="mt-1 block w-full rounded-lg border-gray-300 shadow-sm p-2"
              required
            >
              <option value="" disabled>Select Engine Type</option>
              {dropdowns.engineTypes.map((type) => (
                <option key={type} value={type}>
                  {type}
                </option>
              ))}
            </select>
          </div>

          {/* Engine/Battery Capacity */}
          <div>
            <label className="block text-sm font-medium text-gray-700">
              Engine/Battery Capacity
            </label>
            <input
              type="text"
              name="engine_battery_capacity"
              placeholder="e.g. 200cc / 60.48 kWh"
              value={vehicleData.engine_battery_capacity}
              onChange={handleVehicleChange}
              className="mt-1 block w-full rounded-lg border-gray-300 shadow-sm p-2"
              required
            />
          </div>

          {/* Description */}
          <div>
            <label className="block text-sm font-medium text-gray-700">Description</label>
            <textarea
              name="description"
              placeholder="Optional details about your vehicle"
              value={listingData.description}
              onChange={handleListingChange}
              className="mt-1 block w-full rounded-lg border-gray-300 shadow-sm p-2"
            />
          </div>

          {/* Submit Button */}
          <button
            type="submit"
            disabled={isSubmitting}
            className="w-full flex justify-center items-center px-4 py-2 bg-teal-600 text-white rounded-lg shadow hover:bg-teal-700 disabled:opacity-70"
          >
            {isSubmitting ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Listing...
              </>
            ) : (
              "List Vehicle"
            )}
          </button>
        </form>
      </div>
    </main>
  );
}