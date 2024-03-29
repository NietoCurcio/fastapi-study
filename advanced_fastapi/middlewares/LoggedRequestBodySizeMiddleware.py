from starlette.requests import Request
from starlette.types import ASGIApp, Receive, Scope, Send
import inspect
import os

class LoggedRequestBodySizeMiddleware:
    def __init__(self, app: ASGIApp, counter: int):
        self.app = app
        self.counter = counter
        print(f"ExtraResponseHeadersMiddleware - counter: {self.counter}")

    async def __call__(self, scope, receive, send):
        print(f"ExtraResponseHeadersMiddleware - {self.counter}")

        if scope["type"] == "lifespan":
            print("LoggedRequestBodySizeMiddleware - lifespan executed")

        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        async def receive_logging_request_body_size():
            print(os.path.abspath(inspect.getfile(receive)))

            message = await receive()
            """
            calling receive multiple times per request or 
            creating Request instances body (only use it in fastapi scope) can hang the server
            """
            assert message["type"] == "http.request"

            body_size = len(message.get("body", b""))

            if not message.get("more_body", False):
                print(f"Size of request body was: {body_size} bytes")

            return message

        # await receive() # hangs the server
        # Request(scope, receive).body() # hangs the server
        await self.app(scope, receive, send)

class DeprecatedLoggedRequestBodySizeMiddleware:
    def __init__(self, app, counter):
        self.app = app
        self.counter = counter
        print(f"LoggedRequestBodySizeMiddleware - middleware 1 - counter: {self.counter}")

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        body_size = 0
        message = await receive()
        body_size += len(message.get("body", b""))
        print("LoggedRequestBodySizeMiddleware - body size", body_size)
        await self.app(scope, receive, send)