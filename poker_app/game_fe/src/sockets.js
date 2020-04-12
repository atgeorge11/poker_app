const createSocket = function (gameName) {
    const socket = new WebSocket(
        'ws://'
        + window.location.host
        + '/ws/game/'
        + gameName
        + '/'
    );

    socket.onopen = function(e) {
        socket.send(JSON.stringify({
            'type': "user_type_request"
        }))
    }

    socket.onmessage = function(e) {
        const message = JSON.parse(e.data);
        const event = new CustomEvent('message', {detail: message})
        document.getElementById("root").dispatchEvent(event)
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