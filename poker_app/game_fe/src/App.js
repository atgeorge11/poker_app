import React from 'react';
import createSocket from './sockets';

function App() {

  let gameName = window.location.href;
  gameName = gameName.match(/gameroom\/(.+)\/$/)[1];
  console.log(gameName);
  const socket = createSocket(gameName);

  return (
    <div className="App">
      GAME!
      <button onClick={() => {socket.send("a message")}}>Send a message</button>
    </div>
  );
}

export default App;
