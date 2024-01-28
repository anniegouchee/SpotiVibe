import React,{ useState, useEffect } from "react";
import WebPlayer from './WebPlayer'

import { createPlaylist } from "./GetSongs";
import MenuAppBar from "./MenuAppBar";
import VideoFeed from "./VideoFeed";

function WebCamPage({ socket, accessToken }) {
  const [playlistId, setplaylistId] = useState('https://open.spotify.com/embed/playlist/2VU6rmEdlLPOmmYPSXXfRM?utm_source=generator&theme=0');
  const [mood, setMood]= useState('Neutral')
  const [songs, setSongs]= useState([]);

  useEffect(() => {
    const playlistID = createPlaylist(songs);
    console.log(`Playlist URL for ${mood}: ${playlistID}`);
    setplaylistId(playlistID);
  }, [songs, mood]);

  return (
    <div>
      <MenuAppBar />
      <div
        style={{
          backgroundColor: '#004225',
          display: 'flex',
          flexDirection: 'row',
          justifyContent: 'center', // Center horizontally
          alignItems: 'center',    // Center vertically
          padding: '20px'          // Add space between components
        }}
      >
        <div style={{ margin: '10px' }}>
          <VideoFeed socket={socket} accessToken={accessToken} moodSetter={setMood} songSetter={setSongs}/>
        </div>
        <div style={{ margin: '10px' }}>
          <WebPlayer playlistId={playlistId} playlistTitle={'Something'} />
        </div>
      </div>
    </div>
  );
}

export default WebCamPage;
