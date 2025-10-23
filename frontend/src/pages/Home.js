import { useNavigate } from "react-router-dom";

function Home() {
  const navigate = useNavigate();

  return (
    <div className="home-container">
      <h1 className="home-title">Welcome to UIC Campus Navigator</h1>
      <h2 className="home-subtitles">Your one stop to all campus related inquiries</h2>
      <button className="next-button" onClick={() => navigate("/next")}>
        Get Started
      </button>
    </div>
  );
}

export default Home;