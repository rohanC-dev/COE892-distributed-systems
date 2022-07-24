import React from 'react'
import {useState, useEffect} from 'react'
import 'bootstrap/dist/css/bootstrap.min.css';
import url from '../url.js'

export default function UpdateMine(){
    const [roverID, onChangeRoverID] = useState("")
    const [commands, onChangeCommands] = useState("")
    const [success, setSuccess] = useState("");

    function sendCommands(){
        fetch(url  + "/rovers/" + roverID + "?commands=" + commands, 
        {
        method: 'PUT',
        headers: {
            Accept: "application/json",
            "Content-Type": "application/json",
          }
        })
        .then((res) => console.log(res))
        .then(setSuccess)
      }


    return(
        <div>
            <h1>Send Commands to Rover</h1>

            <p>rover id</p>
            <input type = "text" name = "rover_id" value = {roverID} onChange = {e => onChangeRoverID(e.target.value)}/>
            <p>commmands</p>
            <input type = "text" name = "commands" value = {commands} onChange = {e => onChangeCommands(e.target.value)}/>
            <br></br>
            <button onClick = {sendCommands}>Send Commands</button>
            <p>response: {JSON.stringify(success)} </p>
        </div>
    )
}