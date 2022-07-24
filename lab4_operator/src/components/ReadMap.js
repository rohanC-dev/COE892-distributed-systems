import React from 'react'
import {useState, useEffect} from 'react'
import 'bootstrap/dist/css/bootstrap.min.css';
import url from '../url.js'

function ReadMap() {
  const [data, setMap] = useState(null)

  const [req, sendReq] = useState("");
  const [loading, setLoading] = useState(false);

  //const url = "http://127.0.0.1:8000";
  function getMap(){
      fetch(url + "/map", 
      {
      method: 'GET',
      headers: {
      'Content-Type':'application/json'},
      })
      .then((res) => res.json())
      .then(setMap)
  }

  useEffect(()=>{
    setLoading(true);
    fetch(url + "/map", 
      {
      method: 'GET',
      headers: {
      'Content-Type':'application/json'},
      })
      .then((res) => res.json())
      .then(setMap)
      .then(() => setLoading(false))
  }, [req])

  if(loading) return <h1>loading...</h1>
  

  return (
    <div>
      <h1>Read Map</h1>
      
       <button onClick = {sendReq}>Get Map</button>
       <p>{JSON.stringify(data)}</p>
       
    </div>
  );
}

export default ReadMap;
