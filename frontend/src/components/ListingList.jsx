import { useEffect, useState } from "react";
import ListingRow from "./ListingRow";

// ---------------------- ListingList Component ----------------------
export default function ListingList({ listingType, location }) {
  // ---------------------- State ----------------------
  const [listings, setListings] = useState([]); // List of vehicle listings
  const [loading, setLoading] = useState(true); // Loading state
  const [err, setErr] = useState(""); // Error state

  // ---------------------- Fetch listings when listingType or location changes ----------------------
  useEffect(() => {
    if (!location) return; // Safeguard: Header initializes location quickly

    const controller = new AbortController(); // To abort fetch if component unmounts

    async function load() {
      setLoading(true);
      setErr(""); // Reset error before fetching
      try {
        // Build API URL with query parameters
        const url = `http://localhost:8000/vehicles/listings?listing_type=${encodeURIComponent(
          listingType
        )}&location=${encodeURIComponent(location)}`;

        const res = await fetch(url, {
          method: "GET",
          credentials: "include", // Include session cookie
          signal: controller.signal, // Allow aborting the fetch
        });

        if (!res.ok) {
          const t = await res.text();
          throw new Error(t || "Failed to fetch listings");
        }

        const data = await res.json();
        setListings(data);
      } catch (e) {
        if (e.name !== "AbortError") {
          console.error(e);
          setErr("Could not load listings. Please try again.");
        }
      } finally {
        setLoading(false);
      }
    }

    load();

    // Cleanup function to abort fetch if component unmounts
    return () => controller.abort();
  }, [listingType, location]);

  // ---------------------- Conditional Rendering ----------------------
  if (loading) return <p className="text-center py-8">Loading listings…</p>;
  if (err) return <p className="text-center text-red-600 py-8">{err}</p>;
  if (!listings.length)
    return <p className="text-center py-8">No Available Listings</p>;

  // ---------------------- Render Listings ----------------------
  return (
    <div className="w-full py-6">
      {listings.map((l) => (
        <ListingRow key={l.id} listing={l} />
      ))}
    </div>
  );
}