import { useState, useEffect } from "react";

function Signup() {
    const [fullname, setFullname] = useState("");
    const [phoneNumber, setPhoneNumber] = useState("");
    const [location, setLocation] = useState("");
    const [password, setPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");

    const [cities, setCities] = useState([]);

    // Fetch cities from the backend
    useEffect(() => {
        fetch("http://localhost:8000/locations")
            .then(res => res.json())
            .then(data => setCities(data))
            .catch(err => console.error("Error fetching cities:", err));
    }, []);

    // Check if passwords match
    const passwordsMatch = password && confirmPassword && password === confirmPassword;

    // Handle form submission  
    const handleSubmit = async (e) => {
        e.preventDefault();

        try {
            const response = await fetch("http://localhost:8000/register", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    fullname: fullname,
                    phone_number: phoneNumber,
                    password: password,
                    default_location: location,
                }),
            });

            const data = await response.json();

            if (!response.ok) {
                alert(`❌ Error: ${data.detail || "Registration failed"}`);
                return;
            }

            alert(`✅ ${data.message}`);
            
            // Reset form after successful registration
            setFullname("");
            setPhoneNumber("");
            setLocation("");
            setPassword("");
            setConfirmPassword("");
        } catch (error) {
            console.error("Registration error:", error);
            alert("Something went wrong! Please try again.");
        }
    };

    return (
        <div className="signup-page max-w-md mx-auto p-4">
            <h1 className="text-2xl font-bold mb-4">Signup into Shuttle</h1>
            <form onSubmit={handleSubmit}>
                <div className="mb-4">
                    <label htmlFor="fullname" className="block text-sm font-medium text-gray-700">
                        Fullname
                    </label>
                    <input
                        type="text"
                        id="fullname"
                        name="fullname"
                        placeholder="e.g. John Smith"
                        value={fullname}
                        onChange={(e) => setFullname(e.target.value)}
                        required
                        className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:border-blue-500 focus:ring-blue-500"
                    />
                </div>

                <div className="mb-4">
                    <label htmlFor="phoneNumber" className="block text-sm font-medium text-gray-700">
                        Mobile Number
                    </label>
                    <input
                        type="tel"
                        id="phoneNumber"
                        name="phoneNumber"
                        placeholder="e.g. +9779841321123"
                        value={phoneNumber}
                        onChange={(e) => setPhoneNumber(e.target.value)}
                        required
                        className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:border-blue-500 focus:ring-blue-500"
                    />
                </div>

                <div className="mb-4">
                    <label htmlFor="location" className="block text-sm font-medium text-gray-700">
                        Location
                    </label>
                    <select
                        id="location"
                        name="location"
                        value={location}
                        onChange={(e) => setLocation(e.target.value)}
                        required
                        className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:border-blue-500 focus:ring-blue-500"
                    >
                        <option value="" disabled>
                            Select a location
                        </option>
                        {cities.map((city) => (
                            <option key={city} value={city}>
                                {city}
                            </option>
                        ))}
                    </select>
                </div>

                <div className="mb-4">
                    <label htmlFor="password" className="block text-sm font-medium text-gray-700">
                        Password
                    </label>
                    <input
                        type="password"
                        id="password"
                        name="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                        className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:border-blue-500 focus:ring-blue-500"
                    />
                </div>

                <div className="mb-4">
                    <label htmlFor="confirmPassword" className="block text-sm font-medium text-gray-700">
                        Confirm Password
                    </label>
                    <input
                        type="password"
                        id="confirmPassword"
                        name="confirmPassword"
                        value={confirmPassword}
                        onChange={(e) => setConfirmPassword(e.target.value)}
                        required
                        className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:border-blue-500 focus:ring-blue-500"
                    />
                </div>

                <button
                    type="submit"
                    disabled={!passwordsMatch}
                    className={`w-full py-2 px-4 rounded-md text-white ${
                        passwordsMatch ? "bg-blue-500 hover:bg-blue-600" : "bg-gray-400 cursor-not-allowed"
                    }`}
                >
                    Sign Up
                </button>
            </form>

            <p className="mt-4">
                Already have an account? <a href="./Login.jsx">Login</a>
            </p>
        </div>
    );
}

export default Signup;