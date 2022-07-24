import React from 'react'
import {useState, useEffect} from 'react'
import 'bootstrap/dist/css/bootstrap.min.css';
import url from '../url.js'

export default function DeleteRover(){
    const [roverID, onChangeRoverID] = useState("")
    const [success, setSuccess] = useState("");
    

    function deleteRover(){
        fetch(url  + "/rovers/" + roverID,
            {
            method: 'DELETE',
            headers: {
                Accept: "application/json",
                "Content-Type": "application/json",
                },
            }
        ).then((res) => res.json())
        .then(setSuccess)
    }

    return(
        <div>
            <h1>Delete Rover</h1>
            <p>id of rover</p>
            <input type = "text" name = "rover_id" value = {roverID} onChange = {e => onChangeRoverID(e.target.value)}/>
            <button onClick = {deleteRover}>Delete Rover</button>
            <p>response: {JSON.stringify(success)} </p>
        </div>
    )
}