import time
import asyncio

from fastapi import FastAPI, Request, BackgroundTasks, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from advanced_fastapi.middlewares import MIDDLEWARES
from advanced_fastapi.lifespan import lifespan
from advanced_fastapi.api.router import api_router

"""
# using app.add_middleware the execution is bottom-up (creates top-down, but the __call__ is bottom-up) 
# https://github.com/encode/starlette/issues/1490#issuecomment-1347199743
"""
app = FastAPI(
    middleware=MIDDLEWARES,
    lifespan=lifespan
)

from fastapi.responses import JSONResponse

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    try:
        if request.scope["type"] == "lifespan":
            print("add_process_time_header - lifespan executed") # never executed

        start_time = time.time()

        print('In app.middleware')
        print(await request.body())
        print(await request.body())
        print(await request.body())
        print(request.url)

        request.state.scope_info_5 = "felipe scope 5"

        if request.headers.get('x-test') == 'x-error':
            raise Exception('Error in app.middleware')

        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response
    except Exception as e:
        return JSONResponse(status_code=401, content={"message": str(e)})

async def write_notification(email: str, message=""):
    await asyncio.sleep(10)
    with open("log.txt", mode="w") as email_file:
        content = f"notification for {email}: {message}"
        email_file.write(content)

@app.get("/send-notification/{email}")
async def send_notification(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(write_notification, email, message="some notification")
    return {"message": "Notification sent in the background"}

@app.post("/files/")
async def create_files(files: list[bytes] = File(description="Multiple files as bytes")):
    return {"file_sizes": [len(file) for file in files]}


@app.post("/uploadfiles/")
async def create_upload_files(files: list[UploadFile] = File(description="Multiple files as UploadFile")):
    for file in files:
        try:
            contents = file.file.read()
            with open(file.filename, 'wb') as f:
                f.write(contents)
        except Exception:
            return {"message": "There was an error uploading the file"}
        finally:
            file.file.close()

    return {"message": f"Successfully uploaded {file.filename}"}


@app.get("/")
async def main():
    content = """
    <body>
    <form action="/files/" enctype="multipart/form-data" method="post">
    <input name="files" type="file" multiple>
    <input type="submit">
    </form>
    <form action="/uploadfiles/" enctype="multipart/form-data" method="post">
    <input name="files" type="file" multiple>
    <input type="submit">
    </form>
    </body>
    """
    return HTMLResponse(content=content)

app.mount("/static", StaticFiles(directory="public", html=True), name="static")

app.include_router(api_router)
