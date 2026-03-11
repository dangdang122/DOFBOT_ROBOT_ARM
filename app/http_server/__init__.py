from fastapi import FastAPI
from .router import router

def create_app():
    app = FastAPI()

    app.include_router(router)

    return app