import React, { useState } from "react"
import { Routes, Route, Link, useLocation } from 'react-router-dom'
import './Transport.css'

function Transport() {
    const location = useLocation();

    const [trainLine, setTrainLine] = useState('');
    const [station, setStation] = useState('');

    const handleTrainChange = (event) =>{
        setTrainLine(event.target.value);
    }
     const handleStaionChange = (event) =>{
        setTrainLine(event.target.value);
    }
    return(
        
        <div className="Title">
            {location.pathname === '/transport' && (
            <header>
                <p>Choose Your Transportation Method</p>
                <p id="subTitle">You can change this later in settings</p>
                <div className="transportOptions">
                    <div className="trainline">
                        <select 
                        id="trainSelect"
                        value={trainLine} 
                        onChange={handleTrainChange}>
                            <option>Train Line</option>
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
                    </div>
                    <div className="stations">
                        <select
                        id="stationSelect"
                        value={station}
                        onChange={handleStaionChange}
                        >
                            <option>Departure Station</option>
                            <option>Chicago OTC</option>
                            <option>Clyborn</option>
                            <option>Irving Park</option>
                            <option>Jefferson Park</option>
                            <option>Norwood Park</option>
                            <option>Edison Park</option>
                            <option>Park Ridge</option>
                            <option>Arlington Park</option>
                        </select>
                    </div>
                </div>
                <nav>
                    <Link to="/transport"><button id='start'>Next</button></Link>
                </nav>
            </header>)}

        </div>
    )
}

export default Transport