import React, { useState, useEffect } from 'react';

function ErrorAlert({ message, onClose }) {
  const [isVisible, setIsVisible] = useState(true);

  // Automatically hide the error after 5 seconds
  useEffect(() => {
    const timer = setTimeout(() => {
      setIsVisible(false);
      onClose();
    }, 5000); // 5000 milliseconds = 5 seconds

    // Clear the timer if the component unmounts
    return () => clearTimeout(timer);
  }, [isVisible, onClose]);

  const handleClose = () => {
    setIsVisible(false);
    onClose();
  };

  return isVisible ? (
    <div className="error-alert">
      <p>{message}</p>
    </div>
  ) : null;
}

export default ErrorAlert;
