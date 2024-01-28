import React,{ useState, useEffect } from "react";
import LoginBar from "./LoginBar";
import SignUp from "./SignUp";
import Login from "./Login";
import Picture from "../assets/cute.png"

function LoginSignUp() {


  return (
    <div >
        <LoginBar />
        <div style={{overflow:"hidden"}}>
            <img src={Picture} width="400" style={{paddingLeft:"150px", paddingTop:"100px"}}></img>

        <div style={{width:"700px", float:"right",  paddingTop:"100px", paddingRight:"100px"}} >
            <div style={{width:30}}/>
            <b style={{fontSize:35, color:'#404040', padding:30}} >Time to VIBE</b>
            <div style={{height:7}}/>

            <div style={{padding:30}}>
                <Login />
            </div>
            {/* <hr></hr> */}
            <div style={{textAlign:"center", overflow:"hidden"}}>
            <b style={{fontSize:20,textAlign:"center", color:'#BEBEBE'}}>OR</b>
            </div>

            <div style={{padding:30}}>
                <SignUp />        
            </div>
            </div>
        </div>
    </div>

  );
}

export default LoginSignUp;
