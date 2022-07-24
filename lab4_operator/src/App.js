import './App.css';
import React from 'react'
import {useState, useEffect} from 'react'
import 'bootstrap/dist/css/bootstrap.min.css';
import ReadMap from './components/ReadMap.js'
import UpdateMap from './components/UpdateMap';
import ReadMines from './components/ReadMines'
import ReadMine from './components/ReadMine';
import DeleteMine from './components/DeleteMine';
import CreateMine from './components/CreateMine';
import UpdateMine from './components/UpdateMine';
import ReadRovers from './components/ReadRovers';
import ReadRover from './components/ReadRover'
import CreateRover from './components/CreateRover'
import DeleteRover from './components/DeleteRover'
import SendCommands from './components/SendCommands'
import DispatchRover from './components/DispatchRover';




function App() {

  return (
    <div className="App">
      <ReadMap/>
      <hr></hr>
      <UpdateMap/>
      <hr></hr>
      <ReadMines/>
      <hr></hr>
      <ReadMine/>
      <hr></hr>
      <DeleteMine/>
      <hr></hr>
      <CreateMine/>
      <hr></hr>
      <UpdateMine/>
      <hr></hr>
      <ReadRovers/>
      <hr></hr>
      <ReadRover/>
      <hr></hr>
      <CreateRover/>
      <hr></hr>
      <DeleteRover/>
      <hr></hr>
      <SendCommands/>
      <hr></hr>
      <DispatchRover/>

    </div>
  );
}

export default App;
