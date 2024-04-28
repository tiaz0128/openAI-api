from fastapi import FastAPI, APIRouter
from importlib import import_module


def create_app():
    app = FastAPI()

    views = ["index", "items"]
    for view_name in views:
        module: APIRouter = import_module(f"src.views.{view_name}.view")
        router = module.router

        app.include_router(router, prefix=f"/api/v1")

    return app
