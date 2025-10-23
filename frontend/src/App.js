import { Routes, Route, Link, useLocation } from 'react-router-dom'
import Transport from './Transport'
import './App.css';

function App() {
  const location = useLocation();
  
  return (
    <div className="App">

      {location.pathname === '/' && (
        <header>
          <div className='Title'>
            <p>Welcome to UIC Campus Navigator</p>
            <p id='subTitle'>Your one stop to all campus related inquires</p>
            <nav>
              <Link to="/transport"><button id='start'>Get Started</button></Link>
            </nav>
          </div>
        </header>
      )}
      
      
      <Routes>
        <Route path="/transport" element={<Transport />} />
        <Route path="/" element={
          <div>
          </div>
        } />
      </Routes>
    </div>
  );
}

export default App;