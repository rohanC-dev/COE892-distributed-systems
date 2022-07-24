import React from 'react'
import {useState, useEffect} from 'react'
import 'bootstrap/dist/css/bootstrap.min.css';
import url from '../url.js'

export default function ReadRovers(){
    const [rovers, setRovers] = useState("")

    function readRovers(){
        fetch(url  + "/rovers",
            {
            method: 'GET',
            headers: {
                Accept: "application/json",
                "Content-Type": "application/json",
                },
            }
        ).then((res) => res.json())
        .then(setRovers)
    }

    return(
        <div>
            <p>{JSON.stringify(rovers.list_of_rovers)}</p>
            <button onClick = {readRovers}> Read Rovers</button>
        </div>
    )
}