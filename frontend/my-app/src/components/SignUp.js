import React,{ useState, useEffect } from "react";
import { TextField, Button, Typography, Box, Modal } from "@mui/material";
import './SignUp.css'
import CustomWebcam from "./CustomWebcam";
import queryString from 'query-string';
import ErrorAlert from "./ErrorComonent";

const CLIENT_ID = '17fcbca3196e4730a4325822e0015f71';
const REDIRECT_URI = 'http://localhost:3000/';
const AUTH_ENDPOINT = 'https://accounts.spotify.com/authorize';
const RESPONSE_TYPE = 'token';

function SignUp({ socket, setAccessToken }) {
    const [UserName, setUserName] = useState("");
    const [password, setPassword] = useState("");
    const [open, setOpen] = React.useState(false);
    const [error, setError] = useState(null);

    useEffect(() => {
        const parsed = queryString.parse(window.location.hash);
        const token = parsed.access_token;

        if (token) {
            console.log(token)
            setAccessToken(token);
            if (socket) {
                socket.emit('spotify_token', token);
            }
            setOpen(true);
            setUserName('');
            setPassword('');
        }
    }, [socket, setAccessToken]);

    const handleUserNameChange = (event) => {
        setUserName(event.target.value);
    };

    useEffect(() => {
        if (socket) {
            socket.on("face_name", (name) => {
                setUserName(name);
            });
        }
    })

    const handlePasswordChange = (event) => {
        setPassword(event.target.value);
    };
    
    const handleCapture = (imageSrc) => {
        if (socket) {
          socket.emit('store_image',  imageSrc);
        }
      };

    const handleSignup = () => {
        if (!UserName) {
          setError('Set Username please!');
        } else {
          if (socket) {
            socket.emit('store_user', UserName);
            const url = `${AUTH_ENDPOINT}?client_id=${CLIENT_ID}&redirect_uri=${REDIRECT_URI}&response_type=${RESPONSE_TYPE}`;
            window.location.href = url;
          }
        }
    };

    const closeModal = () => setOpen(false);

    const style = {
        position: 'absolute',
        top: '50%',
        left: '50%',
        transform: 'translate(-50%, -50%)',
        width: 1000,
        bgcolor: 'background.paper',
        p: 4,
      };


  return (
    <div>
          {error && <ErrorAlert message={error} onClose={() => setError(null)} />}
          <div className="container">
              <div className="input">
                  <TextField fullWidth id="UserName-input" label="UserName" variant="outlined"
                      value={UserName}
                      onChange={handleUserNameChange}
                  />
              </div>

              <div className="submit">
                        <Button  variant="contained" color="primary" disableElevation
                        onClick={handleSignup}>
                            SIGN UP       
                        </Button>
            </div>
          </div>

          <Modal
              open={open}
              aria-labelledby="modal-modal-title"
              aria-describedby="modal-modal-description"
          >
              <Box sx={style}>
              <CustomWebcam onClose={closeModal} handleCapture={handleCapture} />

              </Box>
          </Modal>

    </div>

  );
}

export default SignUp;