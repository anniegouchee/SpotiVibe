import React,{ useState, useEffect } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import './App.css';
import LoginSignUp from "./components/LoginSignUp";
import WebCamPage from "./components/WebCamPage";

function App() {


  return (
    <Router>
      <Routes>
        <Route path="/" element={<LoginSignUp />} />
        <Route path="/home" element={<WebCamPage />} />
      </Routes>
    </Router>
  );
}

export default App;
