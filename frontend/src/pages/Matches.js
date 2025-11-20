import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import api from "../api";
import { ACCESS_TOKEN } from "../constants";
import "../styles/Welcome.css";

function Matches() {

    const [matches, setMatches] = useState([]);

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

    return (
        <div className="page-center">
            <div className="matches-box">
                <h1>Your Matches</h1>
                <p>Other users who have a similar schedule to you!</p>

                <div className="matches-column">
                    {matches.length > 0 ? (
                        matches.map((m, idx) => (
                            <div key={idx} className="match-item">
                                {m}
                            </div>
                        ))
                    ) : (
                        <p>No matches found.</p>
                    )}
                </div>
            </div>
        </div>
    );
}

export default Matches;