import asyncio
from fastapi import APIRouter, Request, Response
from fastapi.responses import PlainTextResponse

root_router = APIRouter()

print(root_router.route_class)

@root_router.get("/")
async def root(request: Request) -> Response:
    print("root log")
    print(request.scope['scope-info-1'])
    print(request.scope['scope-info-2'])
    print(request.scope['scope-info-3'])
    print(request.state.scope_info_4)
    print(request.scope['scope-info-38'])
    print(request.state.scope_info_5)
    await asyncio.sleep(1)
    return PlainTextResponse("Hello, world!")

@root_router.post('/')
def dale():
    return PlainTextResponse("Hello, world!")
