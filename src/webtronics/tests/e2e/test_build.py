from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI
from fastapi.testclient import TestClient

from webtronics.api.appbuilder import LifeSpanBuilder, build_app

dummy_router = APIRouter()
indicator = False


class TestLifeSpanBuilder(LifeSpanBuilder):
    @asynccontextmanager
    async def lifespan(self, app: FastAPI):
        global indicator
        indicator = True
        yield
        indicator = False


@dummy_router.get('/')
async def dummy():
    return {'status': 'ok'}


def test_build_app():
    app = build_app(
        dummy_router,
        add_cors_middleware=True,
        lifespanbuilder=TestLifeSpanBuilder(),
    )

    with TestClient(app) as client:
        response = client.get('/')
        assert indicator
        assert response.status_code == 200
        assert response.json() == {'status': 'ok'}
    assert not indicator

    app = build_app(dummy_router, add_cors_middleware=True)
    with TestClient(app) as client:
        assert not indicator
