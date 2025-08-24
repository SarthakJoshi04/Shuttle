import { useState } from 'react';
import Header from '../components/Header';
import ListingList from '../components/ListingList';

export default function Rentals() {
  const [location, setLocation] = useState("Kathmandu");

  return (
    <div className="rentals-page">
      <Header
        title="Rentals"
        subtitle="Find and rent vehicles directly from owners in your area"
        onLocationChange={setLocation}
      />
      <ListingList listingType="RENTAL" location={location} />
    </div>
  );
}