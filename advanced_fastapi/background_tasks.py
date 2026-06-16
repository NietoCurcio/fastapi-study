import threading
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import asyncio

app = FastAPI()


class NameUpdate(BaseModel):
    new_name: str


is_name_changed_event = threading.Event()
current_name = "DefaultName"
is_name_changed_event.set()


async def print_current_name(text, is_name_changed_event):
    while True:
        is_name_changed_event.wait()
        print(f"{text} - Current Name:", current_name)
        await asyncio.sleep(5)


def between_callback2(args, is_name_changed_event):
    asyncio.run(print_current_name(args, is_name_changed_event))


def between_callback3(args, is_name_changed_event):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(print_current_name(args, is_name_changed_event))
    loop.close()


def between_callback4(args, is_name_changed_event):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    asyncio.run_coroutine_threadsafe(
        print_current_name(args, is_name_changed_event), loop
    )
    try:
        loop.run_forever()
    finally:
        loop.close()


background_thread1 = threading.Thread(
    target=asyncio.run,
    args=(print_current_name("some text 1", is_name_changed_event),),
    daemon=True,
)
background_thread2 = threading.Thread(
    target=between_callback2, args=("some text 2", is_name_changed_event), daemon=True
)
background_thread3 = threading.Thread(
    target=between_callback3, args=("some text 3", is_name_changed_event), daemon=True
)
background_thread4 = threading.Thread(
    target=between_callback4, args=("some text 4", is_name_changed_event), daemon=True
)

background_thread1.start()
background_thread2.start()
background_thread3.start()
background_thread4.start()


@app.get("/current_name")
async def get_current_name():
    return {"current_name": current_name}


@app.put("/update_name")
async def update_name(name_update: NameUpdate):
    try:
        is_name_changed_event.clear()
        print("Updating name...")
        await asyncio.sleep(10)
        global current_name
        current_name = name_update.new_name
        is_name_changed_event.set()
        return {"message": "Name updated successfully", "new_name": current_name}
    finally:
        is_name_changed_event.set()


def main():
    uvicorn.run(app)


if __name__ == "__main__":
    main()
