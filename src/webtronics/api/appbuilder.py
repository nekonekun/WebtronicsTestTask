"""Application builder module."""
from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware


class LifeSpanBuilder:
    @asynccontextmanager
    async def lifespan(self, app: FastAPI):
        yield

    def __call__(self):
        return self.lifespan


def build_app(
    *routers: APIRouter,
    swagger_url: str = '/docs',
    redoc_url: str = '/redoc',
    add_cors_middleware: bool = False,
    lifespanbuilder: LifeSpanBuilder = None
) -> FastAPI:
    """Include routers, add CORS middleware and return the app.

    :param routers: APIRouter instances
    :param swagger_url: Swagger URL
    :param redoc_url: Redocly URL
    :param add_cors_middleware: add or not CORS middleware. False by default
    :param lifespanbuilder:
    :return:
    """
    if not lifespanbuilder:
        lifespanbuilder = LifeSpanBuilder()
    app = FastAPI(
        docs_url=swagger_url, redoc_url=redoc_url, lifespan=lifespanbuilder()
    )
    if add_cors_middleware:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=['*'],
            allow_credentials=True,
            allow_methods=['*'],
            allow_headers=['*'],
        )
    for router in routers:
        app.include_router(router)

    return app
