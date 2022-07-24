import React from 'react'
import {useState, useEffect} from 'react'
import 'bootstrap/dist/css/bootstrap.min.css';
import url from '../url.js'

export default function UpdateMine(){
    const [mineID, onChangeMineID] = useState("")
    const [coordinates, onChangeCoordinates] = useState("")
    const [serialNumber, onChangeSerialNumber] = useState("")
    
    const [success, setSuccess] = useState("");

    function updateMine(){
        fetch(url  + "/mines/" + mineID + "?coordinates=" + coordinates + "&serial_number=" + serialNumber, 
        {
        method: 'PUT',
        headers: {
            Accept: "application/json",
            "Content-Type": "application/json",
          },
        body: JSON.stringify({mine_id: mineID, coordinates: coordinates, serial_number: serialNumber})
        
        })
        .then((res) => console.log(res))
        .then(setSuccess)
      }

    return(
        <div>
            <h1>Update Mine</h1>

            <p>mine id (required)</p>
            <input type = "text" name = "mine_id" value = {mineID} onChange = {e => onChangeMineID(e.target.value)}/>
            <p>coordinates</p>
            <input type = "text" name = "coordinates" value = {coordinates} onChange = {e => onChangeCoordinates(e.target.value)}/>
            <p>serial_number</p>
            <input type = "text" name = "serial_number" value = {serialNumber} onChange = {e => onChangeSerialNumber(e.target.value)}/>
            <br></br>
            <button onClick = {updateMine}>Update Mine</button>
            <p>response: {JSON.stringify(success)} </p>
        </div>
    )
}