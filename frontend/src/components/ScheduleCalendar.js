import React from "react";
import { Calendar, momentLocalizer } from "react-big-calendar";
import moment from "moment";
import "react-big-calendar/lib/css/react-big-calendar.css";
import "../styles/schedule.css" 
const localizer = momentLocalizer(moment);

function ScheduleCalendar({ events }) {
  return (
    <div className="calendar-container">
      <Calendar
        localizer={localizer}
        events={events}
        startAccessor="start"
        endAccessor="end"
        views={['week']}
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
      />
    </div>
  );
}

export default ScheduleCalendar;