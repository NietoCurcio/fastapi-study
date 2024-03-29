
from starlette.types import ASGIApp, Receive, Scope, Send
from starlette.datastructures import MutableHeaders

class ExtraResponseHeadersMiddleware:
    def __init__(self, app: ASGIApp, headers: list[tuple[str, str]], counter: int):
        self.app = app
        self.headers = headers
        self.counter = counter
        print(f"ExtraResponseHeadersMiddleware - counter: {self.counter}")

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        print(f"ExtraResponseHeadersMiddleware - {self.counter}")

        if scope["type"] == "lifespan":
            print("ExtraResponseHeadersMiddleware - lifespan executed")

        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        async def send_with_extra_headers(message):
            if message["type"] == "http.response.start":
                headers = MutableHeaders(scope=message)
                for key, value in self.headers:
                    headers.append(key, value)
            await send(message)

        scope['scope-info-38'] = {'felipe': 'felipe scope 38'}
        await self.app(scope, receive, send_with_extra_headers)