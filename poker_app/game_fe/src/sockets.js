const createSocket = function (gameName) {
    const socket = new WebSocket(
        'ws://'
        + window.location.host
        + '/ws/game/'
        + gameName
        + '/'
    );

    socket.onmessage = function(e) {
        console.log(JSON.parse(e.data));
    }

    socket.onclose = function(e) {
        console.error("Chat socket closed unexpectedly");
    }

    const socketController = {};

    socketController.send = function (message) {
        socket.send(JSON.stringify(message));
    }

    return socketController;

}

export default createSocket;