import React from 'react'
import {useState, useEffect} from 'react'
import 'bootstrap/dist/css/bootstrap.min.css';
import url from '../url.js'

export default function DeleteMine(){
    const [mineID, onChangeMineID] = useState("")
    const [success, setSuccess] = useState("");
    

    function deleteMine(){
        fetch(url  + "/mines/" + mineID,
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
            <h1>Delete Mine</h1>
            <p>id of mine</p>
            <input type = "text" name = "mine_id" value = {mineID} onChange = {e => onChangeMineID(e.target.value)}/>
            <button onClick = {deleteMine}>Delete Mine</button>
            <p>response: {JSON.stringify(success)} </p>
        </div> 
    );
}