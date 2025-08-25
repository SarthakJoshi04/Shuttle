import { Routes, Route } from 'react-router-dom';

// Import all page components
import Home from '../pages/home';
import Rentals from '../pages/Rentals';
import Marketplace from '../pages/Marketplace';
import ReportVehicle from '../pages/ReportVehicle';
import Signup from '../pages/Signup';
import Login from '../pages/Login';
import ListVehicle from '../pages/ListVehicle';

// ---------------------- AppRoutes Component ----------------------
export default function AppRoutes() {
  return (
    // ---------------------- Define all routes ----------------------
    <Routes>
        {/* Home Page */}
        <Route path="/" element={<Home />} />

        {/* Rentals Page */}
        <Route path="/rentals" element={<Rentals />} />

        {/* Marketplace Page */}
        <Route path="/marketplace" element={<Marketplace />} />

        {/* Report Vehicle Page */}
        <Route path="/report" element={<ReportVehicle />} />

        {/* Page for listing a new vehicle (only accessible for logged-in users) */}
        <Route path="/list-vehicle" element={<ListVehicle />} />

        {/* Signup Page */}
        <Route path="/signup" element={<Signup />} />

        {/* Login Page */}
        <Route path="/login" element={<Login />} />
    </Routes>
  );
}