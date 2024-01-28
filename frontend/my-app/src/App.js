import React,{ useState, useEffect } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import './App.css';
import LoginSignUp from "./components/LoginSignUp";
import WebCamPage from "./components/WebCamPage";
import io from 'socket.io-client';

function App() {
  const [socket, setSocket] = useState(null);
  const [accessToken, setAccessToken] = useState('');

  useEffect(() => {
    const newSocket = io.connect('http://localhost:4999');
    setSocket(newSocket);
    return () => newSocket.disconnect();
  }, [accessToken]);

  return (
    <Router>
      <Routes>
        <Route path="/" element={<LoginSignUp socket={socket} setAccessToken={setAccessToken}/>} />
        <Route path="/home" element={<WebCamPage />} />
      </Routes>
    </Router>
  );
}

export default App;