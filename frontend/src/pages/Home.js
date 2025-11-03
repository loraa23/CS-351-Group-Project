import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import api from "../api";
import { ACCESS_TOKEN } from "../constants";

// import "../styles/App.css"

function Home() {

    // schedule upload states
    const [file, setFile] = useState(null)
    const [schedules, setSchedules] = useState([])

    // transport selection states
    const [trainLine, setTrainLine] = useState("");
    const [station, setStation] = useState("");

    // transport selection handlers
    const handleTrainChange = (event) =>{
        setTrainLine(event.target.value);
    }
    const handleStationChange = (event) =>{
        setTrainLine(event.target.value);
    }

    // fetch uploaded schedules from this user
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

    // schedule upload handler
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
        } catch (error) {
            console.error("Upload error:", error);
            alert("Failed to upload schedule.");
        }
    };

    return (
    <div>
        <div className="page-container">
            

            <section className="upload-section">
                <h2>Upload Your UIC Schedule (.ics)</h2>

                <form onSubmit={handleSubmit} className="form-container">
                    <div className="file-upload">
                        <input
                            className="form-input"
                            type="file"
                            accept=".ics"
                            onChange={(e) => setFile(e.target.files[0])}
                            required
                        />
                        <button className="form-button" type="submit">Upload</button>
                    </div>
                </form>
            </section>

            <section className="transport-section">
                <header className="Title">
                    <p id="subTitle"> Choose Your Transportation Method</p>
                    <p> You can change this later in settings</p>
                </header>
                <div className="transportOptions">
                <div className="trainline">
                    <select id="trainSelect" value={trainLine} onChange={handleTrainChange}>
                    <option value="">Train Line</option>
                    <option value="BNSF">BNSF (BNSF)</option>
                    <option value="HC">Heritage Corridor (HC)</option>
                    <option value="ME">Metra Electric (ME)</option>
                    <option value="MD-N">Milwaukee District North (MD-N)</option>
                    <option value="MD-W">Milwaukee District West (MD-W)</option>
                    <option value="NCS">North Central Service (NCS)</option>
                    <option value="RI">Rock Island (RI)</option>
                    <option value="SWS">SouthWest Service (SWS)</option>
                    <option value="UP-N">Union Pacific North (UP-N)</option>
                    <option value="UP-NW">Union Pacific Northwest (UP-NW)</option>
                    <option value="UP-W">Union Pacific West (UP-W)</option>
                    </select>
                </div>

                <div className="stations">
                    <select id="stationSelect" value={station} onChange={handleStationChange}>
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
        </div>
        

        <nav>
            <Link to="/Logout"><button id="back">Logout</button></Link>
            <Link to="/Schedule"><button id="next">Generate Schedule</button></Link>
        </nav>
    </div>
  );
}

export default Home