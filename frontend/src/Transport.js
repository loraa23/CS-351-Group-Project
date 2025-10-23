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
                            <option>Ogilvie Transportation Center</option>
                            <option>Chicago Transit Authority(CTA)</option>
                            <option>Chicago Union Station</option>
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