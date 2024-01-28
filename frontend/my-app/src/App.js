import React,{ useState, useEffect } from "react";
import './App.css';
import WebPlayer from './components/WebPlayer'
import { createPlaylist } from "./components/GetSongs";
import playlists from "./data/playlists";

function App() {
  const [playlistId, setplaylistId] = useState('https://open.spotify.com/embed/playlist/2VU6rmEdlLPOmmYPSXXfRM?utm_source=generator&theme=0');
  const [mood, setMood]= useState('Neutral')

  useEffect(() => {
    const playlistID = playlists[mood];
    console.log(`Playlist URL for ${mood}: ${playlistID}`);
    setplaylistId(playlistID);
  }, [mood]); // The dependency array ensures the effect runs when mood changes


  const handleMoodChange = (newMood) => {
    setMood(newMood);
  }

  return (
    <div>
      <WebPlayer
        playlistId={playlistId}
        playlistTitle={'Something'}
      />
<button onClick={() => handleMoodChange('Sad')}>Button</button>

    </div>
  );
}

export default App;
