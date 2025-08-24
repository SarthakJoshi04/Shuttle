import AppRoutes from './routes/Routes';
import Navbar from './components/Navbar';
import Footer from './components/footer';
import './App.css';
import './index.css';

export default function App() {
  
  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      <div className="flex-grow">
        <AppRoutes />
      </div>
      <Footer />
    </div>
    
  )
}