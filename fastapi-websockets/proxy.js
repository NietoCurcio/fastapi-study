// Install the http-proxy library using the command:
// npm install http-proxy --save

const httpProxy = require('http-proxy');
const http = require('http');

// Create a proxy server instance
const proxy = httpProxy.createProxyServer({
    ws: true // Enable WebSocket proxying
});

// Define the target URL
const target = 'ws://127.0.0.1:8000';

// Create the proxy server
const server = http.createServer((req, res) => {
    console.log(`Proxying HTTP request to: ${target}${req.url}`);
    proxy.web(req, res, { target }, (err) => {
        console.error('Error proxying HTTP request:', err);
        res.writeHead(500, { 'Content-Type': 'text/plain' });
        res.end('An error occurred while proxying the request.');
    });
});

// Handle WebSocket connections
server.on('upgrade', (req, socket, head) => {
    console.log(`Proxying WebSocket request to: ${target}${req.url}`);
    proxy.ws(req, socket, head, { target }, (err) => {
        console.error('Error proxying WebSocket request:', err);
    });
});

// Start the server on port 8001
server.listen(8001, '127.0.0.1', () => {
    console.log('Proxy server is running at http://127.0.0.1:8001');
    console.log(`Forwarding WebSocket requests to ${target}`);
});
