import { useContext, useState } from "react";
import { Link, useLocation } from "react-router-dom";
import { User } from "lucide-react";
import { AuthContext } from "../context/AuthContext";

export default function Navbar() {
  const { user, logout } = useContext(AuthContext);
  const location = useLocation();
  const [dropdownOpen, setDropdownOpen] = useState(false);

  const toggleDropdown = () => setDropdownOpen((prev) => !prev);

  const navLinks = [
    { name: "Home", href: "/" },
    { name: "Rentals", href: "/rentals" },
    { name: "Marketplace", href: "/marketplace" },
    { name: "Report", href: "/report" },
  ];

  return (
    <header className="bg-white shadow-sm">
      <div className="max-w-6xl mx-auto px-4">
        <div className="flex justify-between items-center h-16">
          <Link to="/" className="text-2xl font-bold text-teal-600">
            Shuttle
          </Link>

          <nav className="flex space-x-8">
            {navLinks.map((link) => (
              <Link
                key={link.name}
                to={link.href}
                className={`text-sm font-medium transition-colors hover:text-teal-600 ${
                  location.pathname === link.href ? "text-teal-600" : "text-gray-600"
                }`}
              >
                {link.name}
              </Link>
            ))}
          </nav>

          <div className="flex items-center space-x-4">
            {user ? (
              <>
                <Link
                    to="/list-vehicle"
                    className="px-4 py-2 bg-teal-600 text-white rounded hover:bg-teal-700 transition duration-200 text-sm"
                  >
                    List Vehicle
                  </Link>

                <div className="relative">
                  <button
                    className="w-8 h-8 rounded-full bg-gray-200 flex items-center justify-center"
                    onClick={toggleDropdown}
                  >
                    <User className="h-5 w-5 text-gray-700" />
                  </button>

                  {dropdownOpen && (
                    <div className="absolute right-0 mt-2 w-40 bg-white border rounded shadow-md">
                      <div className="px-4 py-2 w-auto text-sm text-gray-600 font-medium">
                        {user.fullname}
                      </div>
                      <button
                        className="block w-full text-left px-4 py-2 text-sm text-gray-600 hover:text-teal-600"
                        onClick={() => {
                          logout();
                          setDropdownOpen(false);
                        }}
                      >
                        Logout
                      </button>
                    </div>
                  )}
                </div>
              </>
            ) : (
              <>
                <Link
                  to="/login"
                  className="px-4 py-2 text-black rounded hover:bg-gray-200 transition-colors"
                >
                  Login
                </Link>

                <Link
                  to="/signup"
                  className="px-4 py-2 bg-black text-white rounded hover:bg-black/70 transition duration-200"
                >
                  Signup
                </Link>
              </>
            )}
          </div>
        </div>
      </div>
    </header>
  );
}