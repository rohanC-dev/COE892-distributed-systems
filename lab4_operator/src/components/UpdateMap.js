import React from 'react'
import {useState, useEffect} from 'react'
import 'bootstrap/dist/css/bootstrap.min.css';
import url from '../url.js'

function UpdateMap() {
    const [height, onChangeHeight] = useState("");
    const [width, onChangeWidth] = useState("");

  //const url = "http://127.0.0.1:8000";
  function updateMap(){
    fetch(url + "/map?height=" + height + "&width=" + width, 
    {
    method: 'PUT',
    headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
    })
    .then((res) => console.log(res))
  }

  
  return (
    <div>
      <h1>Update Map</h1>
      <p>height</p>
       <input type = "number" name = "height" value = {height} onChange = {e => onChangeHeight(e.target.value)}/>
       <p>width</p>
       <input type = "number" name = "width" value = {width} onChange = {e => onChangeWidth(e.target.value)}/>
        <br></br>
       <button onClick = {updateMap}>Update Map</button>
    </div> 
  );
}

export default UpdateMap;
