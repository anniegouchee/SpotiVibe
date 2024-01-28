import * as React from 'react';
import logo from "../assets/logo.png";
import AccountCircleIcon from '@mui/icons-material/AccountCircle';

export default function ButtonAppBar() {
  return (
    <body>
        <nav class="navbar">
            <div>
                    <img style={{ float: 'left', padding: '10px 1340px 0px 10px' }} src={logo} alt="Logo" width="100"  />
                    <AccountCircleIcon sx={{ padding: 1 }} fontSize="large" color="disabled"/>
            </div>
        </nav>
    </body>
  );
}