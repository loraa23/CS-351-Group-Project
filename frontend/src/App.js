import { BrowserRouter, Routes, Route, Link, useLocation, Navigate } from 'react-router-dom'
import Welcome from './pages/Welcome'
import Login from "./pages/Login"
import Register from "./pages/Register"
import Home from "./pages/Home"
import NotFound from "./pages/NotFound"
import ProtectedRoute from './components/ProtectedRoute'
import Schedule from "./pages/Schedule"
import Matches from "./pages/Matches"
import About from "./pages/About"
import './styles/App.css';

function Logout() {
  localStorage.clear()
  return <Navigate to="/login" />
}

function RegisterAndLogout() {
  localStorage.clear()
  return <Register />
}

function App() {
  const location = useLocation();
  
  return (
    <div className="App">
      <Routes>
        <Route path="/" 
          element={
              <Welcome />
          }
          />
        <Route path="/home" 
          element={
            <ProtectedRoute>
              <Home />
            </ProtectedRoute> 
          } 
        />
        <Route path="/schedule" 
          element={
            <ProtectedRoute>
              <Schedule />
            </ProtectedRoute> 
          } 
        />
        <Route path="/matches" 
          element={
            <ProtectedRoute>
              <Matches />
            </ProtectedRoute> 
          } 
        />
        <Route path="/about"
          element={
            <ProtectedRoute>
              <About />
            </ProtectedRoute>
          }
        />
        <Route path="/login" element={<Login />} />
        <Route path="/logout" element={<Logout />} />
        <Route path="/register" element={<RegisterAndLogout />} />
        <Route path="/*" element={<NotFound />} />
      </Routes>
    </div>
  );
}

export default App;