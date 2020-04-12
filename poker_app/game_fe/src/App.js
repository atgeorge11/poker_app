import React from 'react';
import createSocket from './sockets';
import Game from './components/Game';

const App = props => {

  let gameName = window.location.href;
  gameName = gameName.match(/gameroom\/(.+)\/$/)[1];
  const socket = createSocket(gameName);

  return (
    <div className="App">
      GAME!
      <Game socket={socket}/>
      <button onClick={() => {socket.send({message: "a message"})}}>Send a message</button>
    </div>
  );
}

export default App;
