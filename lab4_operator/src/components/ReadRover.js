import React from 'react'
import {useState, useEffect} from 'react'
import 'bootstrap/dist/css/bootstrap.min.css';
import url from '../url.js'

export default function ReadRover(){
    const [roverID, onChangeRoverID] = useState("")
    const [rover, setRover] = useState("")
    
    function readRover(){
        fetch(url  + "/rovers/" + roverID,
            {
            method: 'GET',
            headers: {
                Accept: "application/json",
                "Content-Type": "application/json",
                }
            }
        ).then((res) => res.json())
        .then(setRover)
    }

    return(
        <div>
            <p>{JSON.stringify(rover)}</p>
            <p>id of rover</p>
            <input type = "text" name = "mine_id" value = {roverID} onChange = {e => onChangeRoverID(e.target.value)}/>
            <button onClick = {readRover}> Read Rover</button>
        </div>
    )
}