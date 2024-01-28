import React,{ useState, useEffect } from "react";
import WebPlayer from './WebPlayer'
import playlists from '../data/playlists'
import MenuAppBar from "./MenuAppBar";
import VideoFeed from "./VideoFeed";

function WebCamPage({ socket, accessToken }) {
  const [playlistId, setplaylistId] = useState('https://open.spotify.com/embed/playlist/2VU6rmEdlLPOmmYPSXXfRM?utm_source=generator&theme=0');
  const [mood, setMood]= useState('Neutral')
  const [songs, setSongs]= useState([]);

  useEffect(() => {
    setplaylistId(playlists[mood]);
  }, [songs, mood]);

  return (
    <div>
      <MenuAppBar />
      <div style={{ display: 'flex', flexDirection: 'column' }}>
        <div style={{ display: 'flex', flexDirection: 'row', alignItems: 'stretch' }}>
          <div style={{ flex: '1', maxHeight: '100vh' }}>
            <VideoFeed socket={socket} accessToken={accessToken} moodSetter={setMood} songSetter={setSongs} />
          </div>
          <div>
            <WebPlayer playlistId={playlistId} playlistTitle={'Something'} />
          </div>
        </div>
      </div>
    </div>
  ); 
}

export default WebCamPage;
