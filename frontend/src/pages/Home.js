import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import api from "../api";
import { ACCESS_TOKEN } from "../constants";
import "../styles/Home.css";
import {ReactComponent as UploadIcon} from './Orion_upload.svg'

function Home() {
  // schedule states
  const [file, setFile] = useState(null);
  const [schedules, setSchedules] = useState([]);
  const [selectedSchedule, setSelectedSchedule] = useState(null);


  //Arrival Train Stations
  //Arrival Train stations
  const chiTrainStns = {
    OTC: {
      'UP-N':"Union Pacific North",
      'UP-NW':"Union Pacific Northwest",
      'UP-W':"Union Pacific West",
    },

    Union: {
      'BNSF': "BNSF",
      'HC':"Heritage Corridor",
      'MD-N': "Milwaukee District North",
      'MD-W': "Milwaukee District West",
      'NCS':"North Central Service",
      'SWS': "SouthWest Service",
    },

    Other: {
      'ME': "Metra Electric",
      'RI' :"Rock Island"
    }
  }

  // transport selection states
   const [arrivalTrainStation, setArrivalTrainStation] = useState("");
  const [trainLine, setTrainLine] = useState("");
  const [station, setStation] = useState("");
  const [stations, setStations] = useState([]);

  // fetch uploaded schedules
  useEffect(() => {
    const fetchSchedules = async () => {
      try {
        const res = await api.get("/api/schedules/");
        setSchedules(res.data);
      } catch (error) {
        console.error("Error fetching schedules:", error);
      }
    };
    fetchSchedules();
  }, []);

  // upload new schedule
  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) return alert("Please select a file to upload");

    const token = localStorage.getItem(ACCESS_TOKEN);
    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await api.post("/api/schedules/", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
          Authorization: `Bearer ${token}`,
        },
      });
      setSchedules((prev) => [...prev, res.data]);
      setFile(null);
      setSelectedSchedule(res.data); // auto-select uploaded file
    } catch (error) {
      console.error("Upload error:", error);
      alert("Failed to upload schedule.");
    }
  };

  // delete a schedule
  const handleDelete = async (id) => {
    if (!id) return alert("Schedule ID is missing!");
    if (!window.confirm("Are you sure you want to delete this schedule?")) return;
    const token = localStorage.getItem(ACCESS_TOKEN);

    try {
      await api.delete(`/api/schedules/delete/${id}/`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setSchedules((prev) => prev.filter((s) => s.id !== id));
      if (selectedSchedule?.id === id) setSelectedSchedule(null);
    } catch (err) {
      console.error(err);
      alert("Failed to delete schedule.");
    }
  };

  // transport selection handlers
  const handleStationChange = (event) => {
    setStation(event.target.value);
  };

  // fetch train stations for given line
  const handleTrainChange = async (e) => {
    const line = e.target.value;
    setTrainLine(line);

    if (line) {
        try {
        const res = await api.get(`/api/metra/stations/${line}/`);
        setStations(res.data);
        } catch (err) {
        console.error("Failed to load stations:", err);
        }
    } else {
        setStations([]);
    }

    setStation(""); // reset selected station
    };

  return (
    <div className="page-container">
      {/* Upload Section */}
      <div className="home-menu">
          <ul>
            <Link to="/Logout">
              <li>Logout</li>
            </Link>
            <Link to="/About">
              <li>About</li>
            </Link>
            
          </ul>
      </div>
      <section className="upload">
        <h2>Upload Your UIC Schedule (.ics)</h2>
        <form onSubmit={handleSubmit} className="upload-container">
          <div className="upload-file">
            <input
              type="file"
              accept=".ics"
              onChange={(e) => setFile(e.target.files[0])}
              style={{display: 'none'}}
              id="Inputfile"
            />
            <label
              htmlFor="Inputfile"
              id="upload-icon"
            >
              <UploadIcon width="40" height="40"/>
              
            </label>
            {file && <span id='fileSpan'><p>{file.name}</p></span>}
            
            <button type="submit">Upload</button>
          </div>
        </form>

        {/* Previously uploaded schedules */}
        <h3>Or select a previously uploaded schedule</h3>
        <select
          value={selectedSchedule?.id || ""}
          onChange={(e) => {
            const schedule = schedules.find(
              (s) => s.id === parseInt(e.target.value)
            );
            setSelectedSchedule(schedule);
          }}
        >
          <option value="">-- Select a schedule --</option>
          {schedules.map((s) => (
            <option key={s.id} value={s.id}>
                {s.title}
            </option>
          ))}
        </select>

        <ul>
          {schedules.map((s) => (
            <li key={s.id}>
              {s.title} — {new Date(s.uploaded_at).toLocaleString()}
              <button
                style={{ marginLeft: "15px"}}
                onClick={() => handleDelete(s.id)}
              >
                Delete
              </button>
            </li>
          ))}
        </ul>
      </section>

      {/* Transport Section */}
      <section className="transport-section">
        <header className="transport-Title">
          <p>Select Your Train Stations</p>
          <p id="transport-subTitle">You may change this later</p>
        </header>
        <div className="transportOptions">
          <div className="arrivalTrainStation">
            <p>Chicago Arrival Station:</p>
            <select value={arrivalTrainStation} onChange={(e) => setArrivalTrainStation(e.target.value)}>
              <option value={""}>Arrival Train Station </option>
              <option value={"OTC"}>Ogilvie Transportation Station</option>
              <option value={"Union"}>Chicago Union Station</option>
              <option value={"Other"}>Other</option>
            </select>
          </div>
          <div className="trainline">
            <p>Train Line: </p>
            <select value={trainLine} onChange={handleTrainChange}>
              
              <option value="">Train Line</option>
              {arrivalTrainStation && 
                Object.entries(chiTrainStns[arrivalTrainStation]).map(([key, value]) =>(
                  <option value={key}>{value}</option>
                ))}
            </select>
          </div>
          <div className="stations">
            <p>Departure Stations: </p>
            <select value={station} onChange={handleStationChange}>
                <option value="">Depature Station</option>
                {stations.map((s, idx) => (
                    <option key={idx} value={s}>
                      {s}
                    </option>
                ))}
            </select>
          </div>
        </div>
      </section>

      {/* Navigation */}
      <nav>
        <Link to="/Schedule" state={{ 
            scheduleId: selectedSchedule?.id, 
            trainLine: trainLine,
            station: station}}
        >
          <button id="generateSch" disabled={!selectedSchedule || !trainLine || !station}>
            Generate
          </button>
        </Link>
      </nav>
    </div>
  );
}

export default Home;
