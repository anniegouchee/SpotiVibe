import Webcam from "react-webcam";
import { useRef, useState, useCallback, Button } from "react";

const CustomWebcam = ({onClose, handleCapture}) => {
    const webcamRef = useRef(null);
    const [imgSrc, setImgSrc] = useState(null);

    const capture = useCallback(() => {
        const imageSrc = webcamRef.current.getScreenshot();
        handleCapture(imageSrc);
        onClose();
    }, [onClose]);

  return (
    <div className="container">
    `{imgSrc ? (
        <img src={imgSrc} alt="webcam" />
      ) : (
        <Webcam height={600} width={1000} ref={webcamRef} />
      )}
      <div className="btn-container">
      <button onClick={capture}>Capture photo</button>
      </div>
    </div>
  );
};

export default CustomWebcam;