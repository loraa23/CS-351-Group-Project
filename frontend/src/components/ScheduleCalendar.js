import React from "react";
import { Calendar, momentLocalizer } from "react-big-calendar";
import moment from "moment";
import "react-big-calendar/lib/css/react-big-calendar.css";
import "../styles/Calendar.css";

const localizer = momentLocalizer(moment);

function ScheduleCalendar({ events }) {
  const eventStyleGetter = (event) => {
    return {
      className: event.type === "commute" ? "commute-event" : "default-event",
      // style: {
      //   width: "100%", 
      //   left: "0%",
      //   right: "0%",
      // }
    }
  };

  const CustomEvent = ({ event }) => {
    return (
      <div style={{ fontWeight: "bold" }}>
        {event.title}
      </div>
    );
  };


  return (
    // <div style={{
    //     display: "flex",
    //     flexDirection:"column",
    //     justifyContent: "center", 
    //     alignItems: "center",     
    //     height: "110vh",
    //     width: "200vw",           
    //     boxSizing: "border-box",
    //     padding: "20px",
    //   }}>
    //   <h>Weekly Schedule</h>
      <Calendar
        localizer={localizer}
        events={events}
        eventPropGetter={eventStyleGetter}
        style={{ height: "100vh", width: "150vh", margin: "20px" }}
        startAccessor="start"
        endAccessor="end"
        views={['week']}
        // step={15}
        defaultView="week"
        toolbar={false} // hide navigation
        date={new Date(2025, 0, 6)} // fixed week start (dummy week)
        formats={{
          weekdayFormat: () => "", // hides the real date
          dayFormat: (date, culture, localizer) =>
            localizer.format(date, "dddd") // only show day name
        }}
        min={new Date(2025, 0, 6, 6, 0)}
        max={new Date(2025, 0, 6, 21, 0)}
        components={{ event: CustomEvent}}
      />
    // </div>
  );
}

export default ScheduleCalendar;