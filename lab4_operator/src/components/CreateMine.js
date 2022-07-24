import React from 'react'
import {useState, useEffect} from 'react'
import 'bootstrap/dist/css/bootstrap.min.css';
import url from '../url.js'

export default function CreateMine(){
    const [coordinates, onChangeCoordinates] = useState("")
    const [serialNumber, onChangeSerialNumber] = useState("")

    const [success, setSuccess] = useState("");

    function createMine(){
        fetch(url  + "/mines" + "?coordinates=" + coordinates + "&serial_number=" + serialNumber,
            {
            method: 'POST',
            headers: {
                Accept: "application/json",
                "Content-Type": "application/json",
                }
            }
        ).then((res) => res.json())
        .then(setSuccess)
    }


    return(
        <div>
            <h1>Create Mine</h1>
            <p>coordinates</p>
            <input type = "text" name = "coordinates" value = {coordinates} onChange = {e => onChangeCoordinates(e.target.value)}/>
            <p>serial_number</p>
            <input type = "text" name = "serial_number" value = {serialNumber} onChange = {e => onChangeSerialNumber(e.target.value)}/>
            <button onClick = {createMine}>Create Mine</button>
            <p>response: {JSON.stringify(success)} </p>
        </div> 
    );
}