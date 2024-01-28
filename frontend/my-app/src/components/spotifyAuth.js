import React, { useEffect} from 'react';
import queryString from 'query-string';
import {Button } from "@mui/material";

const CLIENT_ID = '17fcbca3196e4730a4325822e0015f71';
const REDIRECT_URI = 'http://localhost:3000/';
const AUTH_ENDPOINT = 'https://accounts.spotify.com/authorize';
const RESPONSE_TYPE = 'token';

function SpotifyAuth({ socket, setAccessToken }) {
    useEffect(() => {
        const parsed = queryString.parse(window.location.hash);
        const token = parsed.access_token;

        if (token) {
            console.log(token)
            setAccessToken(token);
            if (socket) {
                socket.emit('spotify_token', token);
            }
        }
    }, [socket, setAccessToken]);

    const handleClick = () => {
        const url = `${AUTH_ENDPOINT}?client_id=${CLIENT_ID}&redirect_uri=${REDIRECT_URI}&response_type=${RESPONSE_TYPE}`;
        window.location.href = url;
      };
    
    return (
        <div style={{ position: 'fixed', top: '50%', left: '50%', transform: 'translate(-50%, -50%)' }}>
          <div className="container">
            <div className="submit">
              <Button variant="contained" color="primary" onClick={handleClick} disableElevation>
                Login With Spotify
              </Button>
            </div>
          </div>
        </div>
    );
}

export default SpotifyAuth;
