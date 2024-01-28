import React,{ useState, useEffect} from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import './App.css';
import WebCamPage from "./components/WebCamPage";
import SpotifyAuth from "./components/spotifyAuth";
import io from 'socket.io-client';

function App() {
  const [socket, setSocket] = useState(null);
  
  // const [accessToken, setAccessToken] = useState('');

  // useEffect(() => {
  //     const newSocket = io.connect('http://localhost:4999');
  //     setSocket(newSocket);
  //     return () => newSocket.disconnect();
  // }, [accessToken]);

  return (
    <Router>
      <Routes>
        <Route path="/" element={<LoginSignUp />} />
        <Route path="/home" element={<WebCamPage />} />
      </Routes>
    </Router>
    // <div>
    //   {accessToken ? 
    //     (<WebCamPage socket={socket} setAccessToken={setAccessToken}/>) : 
    //     (<SpotifyAuth socket={socket} setAccessToken={setAccessToken} />)
    //   }
    // </div>
  );
}

export default App;
