from fastapi import FastAPI
import uvicorn

from .routers import sport, event, selection

app = FastAPI()
app.include_router(sport.router)
app.include_router(event.router)
app.include_router(selection.router)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=9000)
