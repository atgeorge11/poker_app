import React from 'react';
import createSocket from './sockets';
import Game from './components/Game';

import './App.css';

const App = props => {

  let gameName = window.location.href;
  let socket = null;
  if (gameName.match(/localhost:8000/)) {
    gameName = gameName.match(/gameroom\/(.+)\/$/)[1];
    socket = createSocket(gameName);
  }

  return (
    <div className="main">
      <span class='table'></span>
      <Game socket={socket}/>
    </div>
  );
}

export default App;
