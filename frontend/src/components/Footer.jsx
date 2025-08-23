import { Link } from "react-router-dom";

export default function Footer() {
  return (
    <footer className="bg-gray-900 text-gray-300">
      <div className="max-w-6xl mx-auto px-6 py-10">
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-8">
 
          <div className="max-w-sm">
            <h3 className="text-2xl font-bold text-white mb-2">Shuttle</h3>
            <p className="text-gray-400 text-sm leading-relaxed">
              A peer-to-peer platform for renting and buying pre-owned vehicles.
            </p>
          </div>

          <div>
            <h4 className="text-lg font-semibold text-white mb-3">Quick Links</h4>
            <ul className="space-y-2">
              <li>
                <Link to="/" className="hover:text-white transition-colors">
                  Home
                </Link>
              </li>
              <li>
                <Link to="/rentals" className="hover:text-white transition-colors">
                  Rentals
                </Link>
              </li>
              <li>
                <Link to="/marketplace" className="hover:text-white transition-colors">
                  Marketplace
                </Link>
              </li>
              <li>
                <Link to="/report" className="hover:text-white transition-colors">
                  Report Vehicle
                </Link>
              </li>
            </ul>
          </div>
        </div>

        <div className="border-t border-gray-800 mt-10 pt-6 text-center text-gray-500 text-sm">
          <p>&copy; {new Date().getFullYear()} Shuttle. All rights reserved.</p>
        </div>
      </div>
    </footer>
  );
}