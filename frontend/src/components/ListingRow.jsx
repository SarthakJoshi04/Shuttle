
export default function ListingRow({ listing }) {
    const imgSrc = listing.image_url
    ? `http://localhost:8000${listing.image_url}`
    : "/placeholder.jpg"; // optional fallback


    // Format price unit
    const priceUnit =
    listing.listing_type === "Rental"
        ? "per hour"
        : listing.listing_type === "Sale"
        ? "total"
        : "";

    return (
        <div className="w-full bg-white shadow-lg rounded-xl p-6 my-6">
            <div className="flex flex-col md:flex-row gap-6">
            {/* Image */}
            <div className="md:w-1/3 w-full flex items-center justify-center">
                <img
                    src={imgSrc}
                    alt={listing.title}
                    className="w-full h-80 object-cover rounded-lg"
                    loading="lazy"
                />
            </div>

            {/* Details */}
            <div className="md:w-2/3 w-full">
                <h2 className="text-3xl font-bold mb-3">{listing.title}</h2>

                {listing.description && (
                <p className="text-gray-800 text-lg mb-4 leading-relaxed">
                    {listing.description}
                </p>
                )}

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-y-2 text-base">
                <div>
                    <span className="font-semibold">Price:</span> NPR {listing.price}{" "}
                    <span className="italic">{priceUnit}</span>
                </div>
                <div>
                    <span className="font-semibold">Location:</span> {listing.location}
                </div>
                <div>
                    <span className="font-semibold">Listing Type:</span>{" "}
                    {listing.listing_type}
                </div>
                <div>
                    <span className="font-semibold">Posted on:</span>{" "}
                    {new Date(listing.created_at).toLocaleString()}
                </div>
                </div>

                <hr className="my-5" />

                <h3 className="text-2xl font-semibold mb-3">Vehicle Details</h3>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-y-2 text-base">
                <div>
                    <span className="font-semibold">Company:</span>{" "}
                    {listing.vehicle.company}
                </div>
                <div>
                    <span className="font-semibold">Model:</span>{" "}
                    {listing.vehicle.model_name}
                </div>
                <div>
                    <span className="font-semibold">Type:</span>{" "}
                    {listing.vehicle.vehicle_type}
                </div>
                <div>
                    <span className="font-semibold">Engine:</span>{" "}
                    {listing.vehicle.engine_type} (
                    {listing.vehicle.engine_battery_capacity})
                </div>
                <div>
                    <span className="font-semibold">Body:</span>{" "}
                    {listing.vehicle.body_type}
                </div>
                <div>
                    <span className="font-semibold">Vehicle No.:</span>{" "}
                    {listing.vehicle.vehicle_no}
                </div>
                </div>

                <hr className="my-5" />

                <h3 className="text-2xl font-semibold mb-3">Posted By</h3>
                <div className="text-base">
                <div>
                    <span className="font-semibold">Name:</span>{" "}
                    {listing.user.fullname}
                </div>
                {listing.user.phone_number ? (
                    <div>
                    <span className="font-semibold">Phone:</span>{" "}
                    {listing.user.phone_number}
                    </div>
                ) : (
                    <div className="italic text-red-500">
                    Login to view phone number
                    </div>
                )}
                </div>
            </div>
            </div>
        </div>
    );
}