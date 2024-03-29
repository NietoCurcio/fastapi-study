from datetime import datetime

from fastapi import Request
from starlette.types import ASGIApp, Receive, Scope, Send
from apscheduler import AsyncScheduler
from apscheduler.triggers.interval import IntervalTrigger

def tick():
    print("Tick, the time is", datetime.now())

class SchedulerMiddleware:
    def __init__(self, app: ASGIApp, scheduler: AsyncScheduler, counter: int) -> None:
        self.app = app
        self.scheduler = scheduler
        self.counter = counter
        print(f"SchedulerMiddleware - counter: {self.counter}")

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        print(f"SchedulerMiddleware - {self.counter}")

        if scope["type"] == "lifespan":
            print("SchedulerMiddleware - lifespan executed")
            async with self.scheduler:
                await self.scheduler.add_schedule(tick, IntervalTrigger(seconds=10), id="tick")
                await self.scheduler.start_in_background()
                await self.app(scope, receive, send)
                return

        scope['scope-info-1'] = "felipe scope 1"
        request = Request(scope)
        
        print(f"Request method: {request.method}")

        scope['scope-info-2'] = "felipe scope 2"
        request.scope['scope-info-3'] = "felipe scope 3"
        print(f"SchedulerMiddleware - {request.scope['scope-info-38']}")
        request.state.scope_info_4 = "felipe scope 4"
        await self.app(scope, receive, send)
