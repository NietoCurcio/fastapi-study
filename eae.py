from starlette.responses import PlainTextResponse
from starlette.requests import Request

async def app(scope, receive, send):
    assert scope['type'] == 'http'
    response = PlainTextResponse('Hello, world!')
    
    req = Request(scope, receive)
    await req.body()

    req1 = Request(scope, receive)
    await req1.body() # hangs the server

    # await receive() # hangs the server
    # await receive()

    await response(scope, receive, send)