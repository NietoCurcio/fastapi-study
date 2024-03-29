import uvicorn

def main():
    uvicorn.run('advanced_fastapi.app:app', reload=True)