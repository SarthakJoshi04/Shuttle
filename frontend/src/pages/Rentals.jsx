import { useState } from "react";
import Header from "../components/Header";
import ListingList from "../components/ListingList";

export default function Rentals() {
  // State to keep track of the selected location for filtering listings
  const [location, setLocation] = useState("Kathmandu");

  return (
    <div className="rentals-page">
      {/* Header component with title, subtitle, and callback for location changes */}
      <Header
        title="Rentals"
        subtitle="Find and rent vehicles directly from owners in your area"
        onLocationChange={setLocation} // Updates the location state when user changes location
      />

      {/* ListingList component displays listings filtered by type and location */}
      <ListingList 
        listingType="RENTAL" // Only show rental listings
        location={location} // Filter listings based on selected location
      />
    </div>
  );
}