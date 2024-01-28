import * as React from 'react';
import logo from "../assets/logo.png";
import './LoginBar.css';

export default function ButtonAppBar() {
  return (
    <body>
        <nav className="navbar">
            <div>
                    <img style={{ float: 'inherit'}} src={logo} alt="Logo" width="200"  />
            </div>
        </nav>
    </body>
  );
}