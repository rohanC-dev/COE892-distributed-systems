import React from 'react'
import {useState, useEffect} from 'react'
import 'bootstrap/dist/css/bootstrap.min.css';
import url from '../url.js'

export default function DispatchRover(){
    const [roverID, onChangeRoverID] = useState("")
    const [traversal, setTraversal] = useState("");

    function dispatchRover(){
        fetch(url  + "/rovers/" + roverID + "/dispatch", 
        {
        method: 'POST',
        headers: {
            Accept: "application/json",
            "Content-Type": "application/json",
          }
        
        })
        .then((res) => res.json())
        .then(setTraversal)
    }
    
    const style = {
        width: 400,
        
    }

    return(
        <div>
            <h1>Dispatch Rover</h1>

            <label>rover id</label>
            <input type = "text" name = "rover_id" value = {roverID} onChange = {e => onChangeRoverID(e.target.value)}/>
    
            <button onClick = {dispatchRover}>Dispatch Rover</button>
            <p style={style}>{JSON.stringify(traversal.traversal_steps)} </p>
            <p style={style}>{JSON.stringify(traversal.traversal_path)} </p>

            
        </div>
    )

}