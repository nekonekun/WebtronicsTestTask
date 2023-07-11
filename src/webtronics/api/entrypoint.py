"""Main API script"""
from contextlib import asynccontextmanager
from typing import Annotated

import typer
import uvicorn
from fastapi import FastAPI
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
)
from redis import asyncio as aioredis
from webtronics.api.adapters.repo import PostRepo, ReactionRepo, UserRepo, ReactionRepoWithCache
from webtronics.api.adapters.emailhunter import EmailHunterAPI
from webtronics.api.appbuilder import LifeSpanBuilder, build_app
from webtronics.api.helpers.auth import AuthHelper
from webtronics.api.helpers.jwt import JWTHelper
from webtronics.api.helpers.misc import get_current_user_factory
from webtronics.api.helpers.poster import PosterHelper
from webtronics.api.helpers.verifier import EmailVerifier
from webtronics.api.routers import posts_router, users_router
from webtronics.api.stubs import auth_stub, get_current_user_stub, poster_stub


class ProductionLifeSpanBuilder(LifeSpanBuilder):
    def __init__(self, database_url: str, secret_key: str, redis_url: str = None, email_hunter_api_key: str = None):
        self.database_url = database_url
        self.secret_key = secret_key
        self.redis_url = redis_url
        self.email_hunter_api_key = email_hunter_api_key

    @asynccontextmanager
    async def lifespan(self, app: FastAPI):
        engine = create_async_engine(self.database_url)

        sessionmaker = async_sessionmaker(engine, expire_on_commit=False)
        user_repo = UserRepo(sessionmaker=sessionmaker)
        post_repo = PostRepo(sessionmaker=sessionmaker)
        if self.redis_url:
            redis_client = aioredis.Redis.from_url(self.redis_url)
            reaction_repo = ReactionRepoWithCache(sessionmaker=sessionmaker,
                                                  redis_client=redis_client)
            await reaction_repo.init_cache()
        else:
            reaction_repo = ReactionRepo(sessionmaker=sessionmaker)

        jwt_helper = JWTHelper(secret_key=self.secret_key)
        if self.email_hunter_api_key:
            email_hunter_api = EmailHunterAPI(api_key=self.email_hunter_api_key)
            email_verifier = EmailVerifier(api=email_hunter_api)
            auth_helper = AuthHelper(
                user_repo=user_repo,
                pwd_context=CryptContext(schemes=['bcrypt'], deprecated='auto'),
                jwt_helper=jwt_helper,
                email_verifier=email_verifier
            )
        else:
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
        yield


def main():
    """API entrypoint"""
    typer.run(_main)


def _main(
    host: Annotated[str, typer.Option()] = '0.0.0.0',
    port: Annotated[int, typer.Option()] = 8000,
    database: Annotated[
        str, typer.Option(envvar='WT_DATABASE_URL')
    ] = 'postgresql+asyncpg://user:pass@127.0.0.1/db',
    redis: Annotated[
        str, typer.Option(envvar='WT_REDIS_URL', help='Optional. Example: redis://127.0.0.1:6379/0')
    ] = None,
    email_hunter_api_key: Annotated[str, typer.Option(envvar='WT_HUNTER_KEY', help='Optional.')] = None,
    secret_key: Annotated[str, typer.Option()] = '$UPER_$ECRET_KEY#',
):
    """Create app and override stub dependencies"""
    app = build_app(
        users_router,
        posts_router,
        lifespanbuilder=ProductionLifeSpanBuilder(database, secret_key, redis, email_hunter_api_key),
    )

    uvicorn_params = {
        'proxy_headers': True,
        'forwarded_allow_ips': '*',
        'host': host,
        'port': port,
    }

    uvicorn.run(app=app, **uvicorn_params)
