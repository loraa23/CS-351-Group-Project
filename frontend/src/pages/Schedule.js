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
          // type: ev.type
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
    <div className= "SchedulePage" style={{
        // display: "flex",
        // flexDirection:"column",
        // justifyContent: "center", 
        // alignItems: "center",     
        // height: "110vh",
        // width: "200vw",           
        // boxSizing: "border-box",
        // padding: "20px",
        padding: "2rem"
      }}>
      
      <div className="Schedulemenu">
        <Link to="/Logout">
          <button id="back">Logout</button>
        </Link>
        <Link to="/Home">
          <button id="back">Back</button>
        </Link>
        <Link to="/Matches">
          <button id="back">Matches</button>
        </Link>
      </div>
      <h1 id="scheduleTitle">Weekly Schedule</h1>
      <ScheduleCalendar events={events} />
    </div>
  );
}

export default Schedule;