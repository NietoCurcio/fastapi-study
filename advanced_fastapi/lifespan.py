from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import FastAPI
from apscheduler import AsyncScheduler
from apscheduler.triggers.interval import IntervalTrigger

def tick2():
    print("Tick2, the time is", datetime.now())

@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler = AsyncScheduler()
    async with scheduler:
        await scheduler.add_schedule(tick2, IntervalTrigger(seconds=5), id="tick2")
        await scheduler.start_in_background()
        yield
        scheduler.shutdown()