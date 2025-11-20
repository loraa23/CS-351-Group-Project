import { useState, useEffect } from "react";
import api from "../api";
import "react-big-calendar/lib/css/react-big-calendar.css";
import ScheduleCalendar from "../components/ScheduleCalendar";
import { useLocation } from "react-router-dom";
import { Link } from "react-router-dom";
import "../styles/schedule.css"
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
    <div  className="SchedulePage" style={{ padding: "2rem" }}>
      <div className="home-menu">
          <ul>
            <Link to="/Logout">
              <li>Logout</li>
            </Link>
            
            <li>Help</li>
            <li>Schedule</li>
            <li>About</li>
          </ul>
      </div>
      <h1 id="scheduleTitle">Weekly Schedule</h1>
      <ScheduleCalendar events={events} />
    </div>
  );
}

export default Schedule;