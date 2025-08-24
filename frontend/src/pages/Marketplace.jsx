import { useState } from 'react';
import Header from '../components/Header';
import ListingList from '../components/ListingList';

export default function Marketplace() {
  const [location, setLocation] = useState("Kathmandu");

  return (
    <div className="marketplace-page">
      <Header
        title="Marketplace"
        subtitle="Browse and buy pre-owned vehicles directly from verified owners"
        onLocationChange={setLocation}
      />
      <ListingList listingType="SALE" location={location} />
    </div>
  );
}