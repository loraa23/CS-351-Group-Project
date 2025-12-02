import React, { useState, useEffect } from "react";
import api from "../api";
import ScheduleCalendar from "../components/ScheduleCalendar"; 
// import "../styles/Welcome.css";

function Matches() {
    const [matches, setMatches] = useState([]);
    const [selectedMatch, setSelectedMatch] = useState(null);
    const [events, setEvents] = useState([]);

    useEffect(() => {
        const fetchMatches = async () => {
            try {
                const res = await api.get("/api/matches/");
                setMatches(res.data);
            } catch (error) {
                console.error("Error fetching matches:", error);
            }
        };
        fetchMatches();
    }, []);

    const handleSelectMatch = async (m) => {
        setSelectedMatch(m);

        try {
            const res = await api.post("/api/schedules/generate/", {
                schedule_id: m.schedule_id,
                train_line: m.train_line,
                station: m.station,
            });

            const formatted = res.data.map(ev => ({
                title: ev.title,
                start: new Date(ev.display_start),
                end: new Date(ev.display_end),
                type: ev.type
            }));
            setEvents(formatted);

        } catch (err) {
            console.error(err);
            alert("Failed to load schedule.");
        }
    };

    return (
        <div style={{
            display: "flex",
            flexDirection: "row",
            width: "100vw",
            height: "100vh",
        }}>
            
            {/* LEFT COLUMN */}
            <div style={{
                width: "30vw",
                borderRight: "1px solid #ccc",
                padding: "20px",
                overflowY: "auto",
            }}>
                <h1>Your Matches</h1>
                <p>Other users who have a similar schedule to you!</p>

                <div className="matches-column">
                    {matches.length > 0 ? (
                        matches.map((m, idx) => (
                            <div 
                                key={idx} 
                                className="match-item"
                                onClick={() => handleSelectMatch(m)}
                                style={{
                                    cursor: "pointer",
                                    padding: "10px",
                                    borderRadius: "8px",
                                    marginBottom: "10px",
                                    background: "#f3f3f3"
                                }}
                            >
                                {m.username} — {m.score}% match
                            </div>
                        ))
                    ) : (
                        <p>No matches found.</p>
                    )}
                </div>
            </div>

            {/* RIGHT COLUMN */}
            <div style={{
                display: "flex",
                flexDirection: "column",
                height: "75%",
                width: "120vw",
                // overflowY: "auto",
            }}>
                {selectedMatch ? (
                    <>
                        <h2>{selectedMatch.username}’s Schedule</h2>

                        <ScheduleCalendar events={events} />

                        <h3  style={{ marginBottom: "0px" }}>Contact Information</h3>
                        <div style={{ display: "flex", gap: "20px", justifyContent: "center"}}>
                            <p style={{fontSize: "15px"}}><strong>Name:</strong> {selectedMatch.username}</p>
                            <p style={{fontSize: "15px"}}><strong>Email:</strong> {selectedMatch.email}</p>
                        </div>
                    </>
                ) : (
                    <h2>Select a match to view their schedule</h2>
                )}
            </div>

        </div>
    );
}

export default Matches;
