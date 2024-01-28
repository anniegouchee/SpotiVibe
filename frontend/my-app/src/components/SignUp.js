import React,{ useState, useEffect } from "react";
import { TextField, Button, Typography, Box, Modal } from "@mui/material";
import './SignUp.css'
import CustomWebcam from "./CustomWebcam";
import { useNavigate } from "react-router-dom";



function SignUp() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [open, setOpen] = React.useState(false);


    const handleEmailChange = (event) => {
        setEmail(event.target.value);
    };

    const handlePasswordChange = (event) => {
        setPassword(event.target.value);
    };

    const handleSignup = () => {
        //console.log(email);
        //console.log(password); 
        setOpen(true);
        setEmail('');
        setPassword('');
    };

    const closeModal = () => {
        setOpen(false);
    }

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

          <div className="container">
              <div className="input">
                  <TextField fullWidth id="email-input" label="Email" variant="outlined"
                      value={email}
                      onChange={handleEmailChange}
                  />
              </div>
              <div className="input">
                  <TextField fullWidth id="password-input" label="Password" variant="outlined"
                      value={password}
                      onChange={handlePasswordChange}
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
              <CustomWebcam onClose={closeModal} />

              </Box>
          </Modal>

    </div>

  );
}

export default SignUp;
