import React from 'react'
import {useState, useEffect} from 'react'
import 'bootstrap/dist/css/bootstrap.min.css';
import url from '../url.js'

export default function ReadMines(){

    const [mines, setMines] = useState(null)

    //const url = "http://127.0.0.1:8000";
    function getMines(){
        fetch(url  + "/mines",
            {
            method: 'GET',
            headers: {
                Accept: "application/json",
                "Content-Type": "application/json",
                },
            }
        )
        .then((res) => res.json())
        .then(setMines)

    }
    
    return (
        <div>
          <h1>Read Mines</h1>
            <p>{JSON.stringify(mines)}</p>
            <button onClick = {getMines}>Get Mines</button>
        </div> 
      );
}