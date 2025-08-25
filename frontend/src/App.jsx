import AppRoutes from './routes/Routes';
import Navbar from './components/Navbar';
import Footer from './components/footer';
import './App.css';
import './index.css';

export default function App() {
  return (
    // Flex column layout to have header, content, and footer
    <div className="min-h-screen flex flex-col">
      
      {/* Navbar at the top */}
      <Navbar />

      {/* Main content area grows to fill available space */}
      <div className="flex-grow">
        <AppRoutes /> {/* Renders the page based on the current route */}
      </div>

      {/* Footer at the bottom */}
      <Footer />
    </div>
  );
}