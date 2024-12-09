from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse

app = FastAPI()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>WebSocket Test</title>
    </head>
    <body>
        <h1>WebSocket Test</h1>
        <form action="" onsubmit="connectWebSocket(event)">
            <input id="messageText" type="text" placeholder="Enter message" autocomplete="off"/>
            <button>Connect</button>
        </form>
        <h2>Messages:</h2>
        <ul id="messages"></ul>
        <script>
            let socket = null;
            function connectWebSocket(event) {
                event.preventDefault();
                const input = document.getElementById("messageText");

                console.log('input:', input.value);
                console.log('socket:', socket);
                if (socket) {
                    console.log('socket.readyState:', socket.readyState);
                }
                console.log('socket.OPEN:', WebSocket.OPEN);
                
                if (!socket || socket.readyState !== WebSocket.OPEN) {
                    console.log("entrei");

                    // socket = new WebSocket(`ws://${location.host}/ws`);
                    socket = new WebSocket(`ws://127.0.0.1:8001/ws`);
                    socket.onopen = () => {
                        const messages = document.getElementById("messages");
                        const connectedMessage = document.createElement("li");
                        connectedMessage.textContent = "WebSocket connection established.";
                        messages.appendChild(connectedMessage);
                    };
                    socket.onmessage = function(event) {
                        console.log('message cae');
                        const messages = document.getElementById("messages");
                        const message = document.createElement("li");
                        message.textContent = event.data;
                        messages.appendChild(message);
                    };
                    socket.onclose = () => {
                        const messages = document.getElementById("messages");
                        const closeMessage = document.createElement("li");
                        closeMessage.textContent = "WebSocket connection closed.";
                        messages.appendChild(closeMessage);
                    };
                    socket.onerror = () => {
                        const messages = document.getElementById("messages");
                        const errorMessage = document.createElement("li");
                        errorMessage.textContent = "WebSocket encountered an error.";
                        messages.appendChild(errorMessage);
                    };
                }
                console.log("PASSEI AQUI CARAI");
                socket.send(input.value);
                input.value = '';
            }
        </script>
    </body>
</html>

"""


@app.get("/")
async def get():
    return HTMLResponse(html)


class SomeClass:
    def __init__(self, websocket):
        self.websocket = websocket

    async def send_data(self):
        await self.websocket.send_text("Hello")


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    print("websocket accepted")
    # show the client info:
    print(websocket.client)
    print(websocket.client_state)
    print(websocket.client_state)
    print(websocket.client.host)
    print(websocket.client.count(0))
    print(websocket.client.port)
    # print(websocket.client.index(0))

    value = 0

    some_class = SomeClass(websocket)

    while True:
        try:
            data = await websocket.receive_text()  # Receive data from client
            print(f"data received: {data}")
            await websocket.send_text(f"Message received: {data}")  # Send response
            # await websocket.send_text(f"Message received: {f'oi-{value}'}")
            # await some_class.send_data()
            # await asyncio.sleep(10)
            value += 1
            raise Exception("Test")

        except Exception:
            break  # Close the connection on error
    await websocket.close()
