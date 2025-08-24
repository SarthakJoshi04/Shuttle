import { Routes, Route } from 'react-router-dom';
import Home from '../pages/home';
import Rentals from '../pages/Rentals';
import Marketplace from '../pages/Marketplace';
import ReportVehicle from '../pages/ReportVehicle';
import Signup from '../pages/Signup'; 
import Login from '../pages/Login';
import ListVehicle from '../pages/ListVehicle';

export default function AppRoutes() {
  return (
    <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/rentals" element={<Rentals />} />
        <Route path="/marketplace" element={<Marketplace />} />
        <Route path="/report" element={<ReportVehicle />} />
        <Route path="/list-vehicle" element={<ListVehicle />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/login" element={<Login />} />
    </Routes>
  );
}