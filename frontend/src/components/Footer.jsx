import { Link } from "react-router-dom";

export default function Footer() {
  return (
    <footer className="bg-gray-900 text-white">
      <div className="max-w-6xl mx-auto px-4 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">

          <div>
            <h3 className="text-xl font-bold mb-4">Shuttle</h3>
            <p className="text-gray-400">
              A peer-to-peer platform for renting and buying pre-owned vehicles.
            </p>
          </div>

          <div>
            <h4 className="text-lg font-semibold mb-4">Quick Links</h4>
            <ul className="space-y-2">
              <li>
                <Link
                  to="/"
                  className="text-gray-400 hover:text-white transition-colors"
                >
                  Home
                </Link>
              </li>
              <li>
                <Link
                  to="/rentals"
                  className="text-gray-400 hover:text-white transition-colors"
                >
                  Rentals
                </Link>
              </li>
              <li>
                <Link
                  to="/marketplace"
                  className="text-gray-400 hover:text-white transition-colors"
                >
                  Marketplace
                </Link>
              </li>
              <li>
                <Link
                  to="/report"
                  className="text-gray-400 hover:text-white transition-colors"
                >
                  Report Vehicle
                </Link>
              </li>
            </ul>
          </div>
        </div>

        <div className="border-t border-gray-800 mt-8 pt-8 text-center text-gray-400">
          <p>&copy; {new Date().getFullYear()} Shuttle. All rights reserved.</p>
        </div>
      </div>
    </footer>
  );
}