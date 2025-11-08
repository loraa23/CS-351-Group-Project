import { useState, useEffect } from "react";
import api from "../api";
import "react-big-calendar/lib/css/react-big-calendar.css";
import ScheduleCalendar from "../components/ScheduleCalendar";

function Schedule() {
  const [events, setEvents] = useState([]);

  useEffect(() => {
    const fetchSchedule = async () => {
      try {
        const res = await api.post("/api/schedules/generate/");
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






// function Schedule() {
//     const [schedules, setSchedules] = useState([])

//     // fetch uploaded schedules from this user
//     useEffect(() => {
//         const fetchSchedules = async () => {
//         try {
//             const res = await api.get("/api/schedules/");
//             setSchedules(res.data);
//         } catch (error) {
//             console.error("Error fetching schedules:", error);
//         }
//         };
//         fetchSchedules();
//     }, []);

//     // currently displays a list of schedules the user uploaded
//     // change this so that this pages displays a schedule 
//     // (grid style Monday - Friday, 5am-10pm, 30 minute increments).
//     return (
//     <section className="schedule-list">
//       <h2>Your Uploaded Schedules</h2>
//       {schedules.length === 0 ? (
//         <p>No schedules uploaded yet.</p>
//       ) : (
//         <ul>
//           {schedules.map((s) => (
//             <li key={s.id}>
//               <strong>{s.title}</strong> —{" "}
//               {new Date(s.uploaded_at).toLocaleString()}
//             </li>
//           ))}
//         </ul>
//       )}
//     </section>
//   );
// }

// export default Schedule