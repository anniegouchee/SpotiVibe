
const token = process.env.SPOTIFY_API_KEY;
//var tracksUri;

async function fetchWebApi(endpoint, method, body) {
  const res = await fetch(`https://api.spotify.com/${endpoint}`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
    method,
    body:JSON.stringify(body)
  });
  return await res.json();
}

const tracksUri = [
  'spotify:track:2dHHgzDwk4BJdRwy9uXhTO','spotify:track:3soKdLpgZNCtYLRsnwxwfB','spotify:track:3vb4YVKrodB9uTuQuOTf1j','spotify:track:2ezY94QlqbDG0aYgKnpy9C','spotify:track:20j7l6tFtc5lynXpbOQg1O','spotify:track:0fX4oNGBWO3dSGUZcVdVV2','spotify:track:3iVSNBsX0ufOh31WL9SnBE','spotify:track:7fX0Vp9q2mtibJF0OkXq9w','spotify:track:5mHdCZtVyb4DcJw8799hZp','spotify:track:3DZQ6mzUkAdHqZWzqxBKIK'
];

export async function createPlaylist(tracksUri){
  const { id: user_id } = await fetchWebApi('v1/me', 'GET')

  const playlist = await fetchWebApi(
    `v1/users/${user_id}/playlists`, 'POST', {
      "name": "My recommendation playlist",
      "description": "Playlist created by the tutorial on developer.spotify.com",
      "public": false
  })

  await fetchWebApi(
    `v1/playlists/${playlist.id}/tracks?uris=${tracksUri.join(',')}`,
    'POST'
  );

  return playlist;
}

// const createdPlaylist = await createPlaylist(tracksUri);
// console.log(createdPlaylist.name, createdPlaylist.id);