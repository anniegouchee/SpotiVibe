import React, { useEffect, useRef, useState } from 'react';
import io from 'socket.io-client';

function VideoFeed({ socket, accessToken, moodSetter, songSetter}) {
    const videoRef = useRef(null);
    const canvasRef = useRef(null);
    const [photoSrc, setPhotoSrc] = useState('');
    const [mood, setMood] = useState('');

    useEffect(() => {
        const socket = io.connect('http://localhost:4999');

        socket.on("connect", () => {
            console.log("Connected...!", socket.connected);
        });

        socket.on("processed_image", (image) => {
            setPhotoSrc(image);
        });

        socket.on("analysis_result", (data) => {
            setMood(data.mood);
            moodSetter(data.mood);
            
            songSetter(data.songs);
            console.log(data.songs);
        });

        if (socket && accessToken) {
            socket.emit('request_songs', { token: accessToken });
        }
  
        if (navigator.mediaDevices.getUserMedia) {
            navigator.mediaDevices
                .getUserMedia({ video: true })
                .then(stream => {
                    if (videoRef.current) {
                        videoRef.current.srcObject = stream;
                    }
                })
                .catch(console.error);
        }

        const FPS = 1;
        const interval = setInterval(() => {
            if (videoRef.current && canvasRef.current) {
                const context = canvasRef.current.getContext('2d');
                const width = videoRef.current.width;
                const height = videoRef.current.height;
                context.drawImage(videoRef.current, 0, 0, width, height);
                const data = canvasRef.current.toDataURL('image/jpeg', 0.5);
                context.clearRect(0, 0, width, height);
                socket.emit('image', data);
            }
        }, 1000 / FPS);

        return () => {
            clearInterval(interval);
            socket.disconnect();
        };
    }, [accessToken, moodSetter, songSetter]);

    return (
        <div style={{ 
          display: 'flex', 
          justifyContent: 'center', 
          alignItems: 'center',
          height: '100vh',
          backgroundColor: '#004225'
        }}>
          <div style={{ position: 'relative', width: '400px', textAlign: 'center' }}>
            <video ref={videoRef} id="videoElement" width="400" height="300" autoPlay />
            <canvas ref={canvasRef} width="400" height="300" style={{ display: 'none' }} />
            {photoSrc && <img src={photoSrc} alt="Processed" style={{ width: '400px', height: '300px' }} />}
      
            <div style={{ position: 'absolute', top: '20px', left: '20px', zIndex: 1 }}>
              <p style={{ color: 'white', fontSize: '16px' }}>Mood: {mood}</p>
            </div>
          </div>
        </div>
      );      
         
}

export default VideoFeed
