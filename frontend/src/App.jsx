import AppRoutes from './routes/Routes'
import './App.css'
import './index.css'

function App() {
  
  return (
    <div className="min-h-screen flex flex-col">
      <div className="flex-grow">
        <AppRoutes />
      </div>
    </div>
    
  )
}

export default App