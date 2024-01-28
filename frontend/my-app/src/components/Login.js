import React,{ useState, useEffect } from "react";
import { Button, Modal, Box } from "@mui/material";
import CustomWebcam from "./CustomWebcam";
import { useNavigate } from "react-router-dom";

function Login() {
    const [open, setOpen] = React.useState(false);
    const navigate = useNavigate();

    const handleLogin = () => {
        setOpen(true);
        navigate("/home");
    };


    const style = {
        position: 'absolute',
        top: '50%',
        left: '50%',
        transform: 'translate(-50%, -50%)',
        width: 400,
        bgcolor: 'background.paper',
        p: 4,
      };


    return (
        <div>
            <Button fullWidth variant="contained" color="primary" disableElevation
                onClick={handleLogin}>
                LOG IN
            </Button>
            <Modal
              open={open}
              aria-labelledby="modal-modal-title"
              aria-describedby="modal-modal-description"
          >
              <Box sx={style}>
              </Box>
          </Modal>

        </div>
        

    );
}

export default Login;
