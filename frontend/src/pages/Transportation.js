import { useState } from "react";


function Transportation() {

  const [line, setLine] = useState("");
  const [station, setStation] = useState("");


  return (
    <div className="transportation-container">
      <h1 className="page-title"> Choose Your Transportation Method</h1>

      <div className="dropdown-row">
        <select
          className="dropdown"
          value={line}
          onChange={(e) => setLine(e.target.value)}
        >
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

        <select
          className="dropdown"
          value={station}
          onChange={(e) => setStation(e.target.value)}
        >
          <option value="">Station</option>
          <option value="Station1">Station 1</option>
          <option value="Station2">Station 2</option>
          <option value="...">...</option>
        </select>
      </div>

      <button className="next-button">Next</button>
    </div>
  );
}

export default Transportation;