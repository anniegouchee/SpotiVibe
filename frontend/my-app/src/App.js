import React,{ useState, useEffect } from "react";
import './App.css';
import WebCamPage from "./components/WebCamPage";
import Login from "./components/Login"; 
import LoginSignUp from "./components/LoginSignUp";

function App() {


  return (
    <div>

    {/* <WebCamPage /> */}
    <LoginSignUp />
    </div>
  );
}

export default App;
