import React,{ useState, useEffect } from "react";
import { Button, Modal, Box } from "@mui/material";
import CustomWebcam from "./CustomWebcam";
import { useNavigate } from "react-router-dom";
import ErrorAlert from "./ErrorComonent";

function Login({ socket}) {
    const [open, setOpen] = React.useState(false);
    const [error, setError] = useState(null);
    const navigate = useNavigate();

    useEffect(() => {
        if (socket) {
            socket.on("login_result", (name) => {
                if (name.names != 'Unknown') {
                    navigate("/home");
                }
                else {
                    setError('Try Again Please');
                }
            });
        }
    })

    const handleLogin = () => {
        setOpen(true);
    };
    const closeModal = () => setOpen(false);

    const handleCapture = (imageSrc) => {
        if (socket) {
          socket.emit('recognize', imageSrc);
        }
      };

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
            <Button fullWidth variant="contained" color="primary" disableElevation onClick={handleLogin}>
                LOG IN
            </Button>
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

export default Login;