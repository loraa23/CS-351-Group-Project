import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import api from "../api";
import { ACCESS_TOKEN } from "../constants";
// import "../styles/Home.css";

function Home() {
  // schedule states
  const [file, setFile] = useState(null);
  const [schedules, setSchedules] = useState([]);
  const [selectedSchedule, setSelectedSchedule] = useState(null);

  // transport selection states
  const [trainLine, setTrainLine] = useState("");
  const [station, setStation] = useState("");

  // transport selection handlers
  const handleTrainChange = (event) => {
    setTrainLine(event.target.value);
  };
  const handleStationChange = (event) => {
    setStation(event.target.value);
  };

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
      alert("File uploaded successfully!");
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

  return (
    <div className="page-container">
      {/* Upload Section */}
      <section className="upload-section">
        <h2>Upload Your UIC Schedule (.ics)</h2>
        <form onSubmit={handleSubmit} className="form-container">
          <div className="file-upload">
            <input
              type="file"
              accept=".ics"
              onChange={(e) => setFile(e.target.files[0])}
            />
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
                style={{ marginLeft: "10px" }}
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
        <header className="Title">
          <p id="subTitle">Choose Your Transportation Method</p>
          <p>You can change this later in settings</p>
        </header>
        <div className="transportOptions">
          <div className="trainline">
            <select value={trainLine} onChange={handleTrainChange}>
              <option value="">Train Line</option>
              <option value="BNSF">BNSF</option>
              <option value="HC">Heritage Corridor</option>
              <option value="ME">Metra Electric</option>
              <option value="MD-N">Milwaukee District North</option>
              <option value="MD-W">Milwaukee District West</option>
              <option value="NCS">North Central Service</option>
              <option value="RI">Rock Island</option>
              <option value="SWS">SouthWest Service</option>
              <option value="UP-N">Union Pacific North</option>
              <option value="UP-NW">Union Pacific Northwest</option>
              <option value="UP-W">Union Pacific West</option>
            </select>
          </div>

          <div className="stations">
            <select value={station} onChange={handleStationChange}>
              <option value="">Departure Station</option>
              <option>Chicago OTC</option>
              <option>Clybourn</option>
              <option>Irving Park</option>
              <option>Jefferson Park</option>
              <option>Norwood Park</option>
              <option>Edison Park</option>
              <option>Park Ridge</option>
              <option>Arlington Park</option>
            </select>
          </div>
        </div>
      </section>

      {/* Navigation */}
      <nav>
        <Link to="/Logout">
          <button id="back">Logout</button>
        </Link>
        <Link
          to="/Schedule"
          state={{ scheduleId: selectedSchedule?.id }}
        >
          <button id="next" disabled={!selectedSchedule}>
            Generate Schedule
          </button>
        </Link>
      </nav>
    </div>
  );
}

export default Home;
