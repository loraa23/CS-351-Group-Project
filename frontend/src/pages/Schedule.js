import { useState, useEffect } from "react";
import api from "../api";
import "react-big-calendar/lib/css/react-big-calendar.css";
import ScheduleCalendar from "../components/ScheduleCalendar";
import { useLocation } from "react-router-dom";

function Schedule() {
  const [events, setEvents] = useState([]);
  const location = useLocation();
  const { scheduleId, trainLine, station } = location.state;

  useEffect(() => {
    const fetchSchedule = async () => {
      try {
        const res = await api.post("/api/schedules/generate/",
          {
            schedule_id: scheduleId,
            train_line: trainLine,
            station: station
          },
        );

        const formatted = res.data.map(ev => ({
          title: ev.title,
          start: new Date(ev.display_start),
          end: new Date(ev.display_end),
        }));
        setEvents(formatted);

      } catch (err) {
        console.error(err);
        alert("Failed to load schedule.");
      }
    };

    fetchSchedule();
  }, []);

  return (
    <div style={{ padding: "2rem" }}>
      <h1>Weekly Schedule</h1>
      <ScheduleCalendar events={events} />
    </div>
  );
}

export default Schedule;