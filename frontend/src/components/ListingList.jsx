import { useEffect, useState } from "react";
import ListingRow from "./ListingRow";

export default function ListingList({ listingType, location }) {
  const [listings, setListings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [err, setErr] = useState("");

  useEffect(() => {
    if (!location) return; // safeguard; Header initializes this quickly

    const controller = new AbortController();

    async function load() {
      setLoading(true);
      setErr("");
      try {
        const url = `http://localhost:8000/vehicles/listings?listing_type=${encodeURIComponent(
          listingType
        )}&location=${encodeURIComponent(location)}`;

        const res = await fetch(url, {
          method: "GET",
          credentials: "include", // send session cookie
          signal: controller.signal,
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
    return () => controller.abort();
  }, [listingType, location]);

  if (loading) return <p className="text-center py-8">Loading listings…</p>;
  if (err) return <p className="text-center text-red-600 py-8">{err}</p>;
  if (!listings.length)
    return <p className="text-center py-8">No Available Listings</p>;

  return (
    <div className="w-full py-6">
      {listings.map((l) => (
        <ListingRow key={l.id} listing={l} />
      ))}
    </div>
  );
}