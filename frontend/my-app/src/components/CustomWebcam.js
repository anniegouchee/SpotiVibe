import Webcam from "react-webcam";
import { useRef, useState, useCallback, Button } from "react";

const CustomWebcam = ({onClose}) => {
    const webcamRef = useRef(null);
    const [imgSrc, setImgSrc] = useState(null);

    const capture = useCallback(() => {
        const imageSrc = webcamRef.current.getScreenshot();
        saveImageLocally(imageSrc);
        onClose();
    }, [onClose]);

    const saveImageLocally = (imageSrc) => {
        const byteCharacters = atob(imageSrc.split(",")[1]);
        const byteNumbers = new Array(byteCharacters.length);
        for (let i = 0; i < byteCharacters.length; i++) {
          byteNumbers[i] = byteCharacters.charCodeAt(i);
        }
        const byteArray = new Uint8Array(byteNumbers);
    
        const blob = new Blob([byteArray], { type: "image/png" });
    
        const link = document.createElement("a");
        link.href = URL.createObjectURL(blob);
        link.download = "./captured_photo.png";
    
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
      };

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