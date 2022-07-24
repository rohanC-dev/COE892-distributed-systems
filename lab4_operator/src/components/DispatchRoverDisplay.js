import React from 'react'
import {useState, useEffect} from 'react'
import 'bootstrap/dist/css/bootstrap.min.css';
import url from '../url.js'

export default function DispatchRoverDisplay(traversal){
    
    
    return(
        <div>
            <ol>
                {traversal.map((comp)=>{
                    return <li>6</li>
                })}
            </ol>
        </div>
    )

}