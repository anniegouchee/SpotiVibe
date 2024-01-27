function WebPlayer (props) {
    const { playlistId, playlistTitle } = props;
 
  return (
    <div className="container">
        <iframe
            title={playlistTitle}
            src={playlistId}
            width="100%"
            height="100%"
            style={{ minHeight: '750px',
            maxWidth: '400px'
           }}
            allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture"
            loading="lazy"
        />
    </div>
  );
}

export default WebPlayer;
