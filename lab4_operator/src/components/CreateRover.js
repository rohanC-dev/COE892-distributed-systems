import React from 'react'
import {useState, useEffect} from 'react'
import 'bootstrap/dist/css/bootstrap.min.css';
import url from '../url.js'

export default function CreateRover(){
    const [commands, onChangeCommands] = useState("")

    const [success, setSuccess] = useState("");

    function createRover(){
        fetch(url  + "/rovers" + "?commands=" + commands,
            {
            method: 'POST',
            headers: {
                Accept: "application/json",
                "Content-Type": "application/json",
                },
            body: JSON.stringify({commands: commands})
            }
        ).then((res) => res.json())
        .then(setSuccess)
    }

    return(
        <div>
            <h1>Create Rover</h1>
            <p>response {JSON.stringify(success)}</p>
            <p>string of commands</p>
            <input type = "text" name = "commands" value = {commands} onChange = {e => onChangeCommands(e.target.value)}/>
            <button onClick = {createRover}>Create Rover</button>
        </div> 
    )
}