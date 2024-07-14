import uvicorn

if __name__ == "__main__":
    uvicorn.run("startapp.asgi:application", reload=True, port=6000)