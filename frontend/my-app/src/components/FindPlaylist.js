
const fs = require('fs');
const jsonFilePath = '../data/playlists.json';

function findPlaylist () {

try {
    const jsonData = fs.readFileSync(jsonFilePath, 'utf-8');
    const data = JSON.parse(jsonData);
      
  } catch (error) {
    console.error('Error reading JSON file:', error);
  }
}
