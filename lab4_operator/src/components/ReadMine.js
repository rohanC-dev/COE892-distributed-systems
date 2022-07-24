import React from 'react'
import {useState, useEffect} from 'react'
import 'bootstrap/dist/css/bootstrap.min.css';
import url from '../url.js'

export default function ReadMine(){

    const [mineID, onChangeMineID] = useState("")
    const [mine, setMine] = useState("")

    //const url = "http://127.0.0.1:8000";
    function getMine(){
        fetch(url  + "/mines/" + mineID,
            {
            method: 'GET',
            headers: {
                Accept: "application/json",
                "Content-Type": "application/json",
                },
            }
        )
        .then((res) => res.json())
        .then(setMine)
    }
    return (
        <div>
          <h1>Read Mine</h1>
            <p>{JSON.stringify(mine)}</p>
            <p>id of mine</p>
            <input type = "text" name = "mine_id" value = {mineID} onChange = {e => onChangeMineID(e.target.value)}/>
            <button onClick = {getMine}>Get Mine</button>
        </div> 
      );
}