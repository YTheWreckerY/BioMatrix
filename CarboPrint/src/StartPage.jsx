import { Link } from "react-router-dom";
import bgVideo from "./background_vid.mp4";
import "./App.css";

export default function StartPage() {
  return (
    <div className="start-container">
      <video autoPlay muted loop playsInline className="bg-video">
        <source src={bgVideo} type="video/mp4" />
      </video>

      {/* Center Content */}
      <div className="start-content">
        <h1 className="start-title">CarboPrint</h1>
        <Link to="/questions">
          <button className="start-btn">Start</button>
        </Link>
      </div>

    </div>
  );
}

