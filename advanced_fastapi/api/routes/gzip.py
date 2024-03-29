from typing import Callable

from fastapi import APIRouter, Request, Response, Body
from fastapi.routing import APIRoute

# more appropriate than LoggedRequestBodySizeMiddleware (since receive multiple times can be a problem)
class GzipRequest(Request):
    async def body(self) -> bytes:
        body = await super().body()
        print('In GzipRequest - body length:', len(body))
        return body

class GzipRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()
        async def custom_route_handler(request: Request) -> Response:
            request = GzipRequest(request.scope, request.receive)
            return await original_route_handler(request)
        return custom_route_handler

gzip_router = APIRouter(route_class=GzipRoute)

@gzip_router.post("/")
async def sum_numbers(request: Request, body = Body()):
    print("FELIPE 1")
    print(body)
    # print(body())
    print(await request.body())
    return 'dale'