"""Main API script"""
from typing import Annotated

import typer
import uvicorn
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
)

from webtronics.api.adapters.repo import PostRepo, UserRepo, ReactionRepo
from webtronics.api.appbuilder import build_app
from webtronics.api.helpers.auth import AuthHelper
from webtronics.api.helpers.jwt import JWTHelper
from webtronics.api.helpers.misc import get_current_user_factory
from webtronics.api.helpers.poster import PosterHelper
from webtronics.api.routers import posts_router, users_router
from webtronics.api.stubs import auth_stub, get_current_user_stub, poster_stub


def main():
    """API entrypoint"""
    typer.run(_main)


def _main(
    host: Annotated[str, typer.Option()] = '0.0.0.0',
    port: Annotated[int, typer.Option()] = 8000,
    database: Annotated[
        str, typer.Option()
    ] = 'postgresql+asyncpg://user:pass@127.0.0.1/db',
    secret_key: Annotated[str, typer.Option()] = '$UPER_$ECRET_KEY#',
):
    """Create app and override stub dependencies"""
    app = build_app(users_router, posts_router)

    uvicorn_params = {
        'proxy_headers': True,
        'forwarded_allow_ips': '*',
        'host': host,
        'port': port,
    }

    engine = create_async_engine(database)

    sessionmaker = async_sessionmaker(engine, expire_on_commit=False)
    user_repo = UserRepo(sessionmaker=sessionmaker)
    post_repo = PostRepo(sessionmaker=sessionmaker)
    reaction_repo = ReactionRepo(sessionmaker=sessionmaker)
    jwt_helper = JWTHelper(secret_key=secret_key)
    auth_helper = AuthHelper(
        user_repo=user_repo,
        pwd_context=CryptContext(schemes=['bcrypt'], deprecated='auto'),
        jwt_helper=jwt_helper,
    )
    get_current_user = get_current_user_factory(user_repo, jwt_helper)
    poster_helper = PosterHelper(post_repo, reaction_repo)

    app.dependency_overrides[auth_stub] = auth_helper
    app.dependency_overrides[get_current_user_stub] = get_current_user
    app.dependency_overrides[poster_stub] = poster_helper

    uvicorn.run(app=app, **uvicorn_params)
