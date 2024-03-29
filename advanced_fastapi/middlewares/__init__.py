from starlette.middleware import Middleware
from apscheduler import AsyncScheduler

from advanced_fastapi.middlewares.ExtraResponseHeadersMiddleware import ExtraResponseHeadersMiddleware
from advanced_fastapi.middlewares.SchedulerMiddleware import SchedulerMiddleware
from advanced_fastapi.middlewares.LoggedRequestBodySizeMiddleware import LoggedRequestBodySizeMiddleware

MIDDLEWARES = [
    Middleware(
        ExtraResponseHeadersMiddleware,
        headers=[("X-Felipe-Example", "Example Felipe Value")],
        counter=1
    ),
    Middleware(LoggedRequestBodySizeMiddleware, counter=2),
    Middleware(SchedulerMiddleware, scheduler=AsyncScheduler(), counter=3),
]
