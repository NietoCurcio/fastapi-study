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
            let reconnectInterval = 5000; // Time (in ms) to wait before attempting a reconnect
            let reconnectTimeout = null;

            function connectWebSocket(event) {
                if (event) {
                    event.preventDefault();
                }

                const input = document.getElementById("messageText");

                console.log('input:', input?.value);
                console.log('socket:', socket);
                if (socket) {
                    console.log('socket.readyState:', socket.readyState);
                }
                console.log('socket.OPEN:', WebSocket.OPEN);

                if (!socket || socket.readyState !== WebSocket.OPEN) {
                    console.log("Attempting to connect...");

                    // socket = new WebSocket(`ws://${location.host}/ws`);
                    socket = new WebSocket(`ws://127.0.0.1:8001/ws`);
                    socket.onopen = () => {
                        console.log("Connection established.");
                        const messages = document.getElementById("messages");
                        const connectedMessage = document.createElement("li");
                        connectedMessage.textContent = "WebSocket connection established.";
                        messages.appendChild(connectedMessage);

                        // Clear any existing reconnect timeout if connected successfully
                        if (reconnectTimeout) {
                            clearTimeout(reconnectTimeout);
                            reconnectTimeout = null;
                        }
                    };
                    socket.onmessage = function(event) {
                        console.log('Message received:', event.data);
                        const messages = document.getElementById("messages");
                        const message = document.createElement("li");
                        message.textContent = event.data;
                        messages.appendChild(message);
                    };
                    socket.onclose = () => {
                        console.log("Connection closed. Attempting to reconnect...");
                        handleReconnect();
                    };
                    socket.onerror = () => {
                        console.log("Connection error. Attempting to reconnect...");
                        handleReconnect();
                    };
                }
                
                if (socket.readyState === WebSocket.OPEN && input) {
                    socket.send(input.value);
                    input.value = '';
                }
            }

            function handleReconnect() {
                const messages = document.getElementById("messages");
                const reconnectMessage = document.createElement("li");
                reconnectMessage.textContent = "WebSocket connection lost. Reconnecting...";
                messages.appendChild(reconnectMessage);

                if (!reconnectTimeout) {
                    reconnectTimeout = setTimeout(() => {
                        console.log("Reconnecting...");
                        connectWebSocket();
                    }, reconnectInterval);
                }
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

    value = 0

    some_class = SomeClass(websocket)

    while True:
        try:
            data = await websocket.receive_text()  # Receive data from client
            print(f"data received: {data}")
            await websocket.send_text(f"Message received: {data}-{value}")  # Send response
            # await websocket.send_text(f"Message received: {f'oi-{value}'}")
            # await some_class.send_data()
            # await asyncio.sleep(10)
            value += 1
            raise Exception("Test")

        except Exception:
            break  # Close the connection on error
    await websocket.close()
