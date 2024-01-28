import React,{ useState, useEffect } from "react";
import { TextField, Button } from "@mui/material";
import './SignUp.css'


function SignUp() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");

    const handleEmailChange = (event) => {
        setEmail(event.target.value);
    };

    const handlePasswordChange = (event) => {
        setPassword(event.target.value);
    };

    const handleSignup = () => {
        //console.log(email);
        //console.log(password); 
        setEmail('');
        setPassword('');
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
                            SIGNUP       
                        </Button>
            </div>:
          </div>

    </div>

  );
}

export default SignUp;
