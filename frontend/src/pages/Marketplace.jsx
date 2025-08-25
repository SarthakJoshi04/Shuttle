import { useState } from "react";
import Header from "../components/Header";
import ListingList from "../components/ListingList";

export default function Marketplace() {
  // State to keep track of the selected location for filtering listings
  const [location, setLocation] = useState("Kathmandu");

  return (
    <div className="marketplace-page">
      {/* Header component with title, subtitle, and callback for location changes */}
      <Header
        title="Marketplace"
        subtitle="Browse and buy pre-owned vehicles directly from verified owners"
        onLocationChange={setLocation} // Updates the location state when user changes location
      />

      {/* ListingList component displays listings filtered by type and location */}
      <ListingList
        listingType="SALE" // Only show sale listings
        location={location} // Filter listings based on selected location
      />
    </div>
  );
}