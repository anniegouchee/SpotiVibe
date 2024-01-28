import React from 'react';
import logo from "../assets/logo.png";
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import './MenuAppBar.css'

export default function MenuAppBar() {
  return (
    <nav className="navbar">
      <div>
        <img src={logo} alt="Logo" width="100" />
        <AccountCircleIcon sx={{ padding: 1.5 }} fontSize="large" color="disabled" />
      </div>
    </nav>
  );
}
