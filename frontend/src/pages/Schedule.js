import { useState, useEffect } from "react";
import api from "../api";

function Schedule() {
    const [schedules, setSchedules] = useState([])

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

    // currently displays a list of schedules the user uploaded
    // change this so that this pages displays a schedule 
    // (grid style Monday - Friday, 5am-10pm, 30 minute increments).
    return (
    <section className="schedule-list">
      <h2>Your Uploaded Schedules</h2>
      {schedules.length === 0 ? (
        <p>No schedules uploaded yet.</p>
      ) : (
        <ul>
          {schedules.map((s) => (
            <li key={s.id}>
              <strong>{s.title}</strong> —{" "}
              {new Date(s.uploaded_at).toLocaleString()}
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}

export default Schedule