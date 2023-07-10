"""Post-related routes"""
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from webtronics.api.exceptions import (
    PosterNotFoundError,
    PosterPermissionError,
)
from webtronics.api.schemas.posts import (
    Post,
    PostCreateRequest,
    PostReactions,
    PostUpdateRequest,
)
from webtronics.api.schemas.users import User
from webtronics.api.stubs import PosterStub, get_current_user_stub, poster_stub

posts_router = APIRouter(
    prefix='/posts',
    tags=['Posts'],
)


@posts_router.post('/', response_model=Post)
async def create_post(
    current_user: Annotated[User, Depends(get_current_user_stub)],
    poster: Annotated[PosterStub, Depends(poster_stub)],
    body: PostCreateRequest,
):
    return await poster.create(
        title=body.title, text=body.text, author_id=current_user.id
    )


@posts_router.get('/', response_model=list[Post])
async def list_posts(
    current_user: Annotated[User, Depends(get_current_user_stub)],
    poster: Annotated[PosterStub, Depends(poster_stub)],
    author_id: Annotated[int | None, Query()] = None,
    offset: Annotated[int, Query()] = 0,
    limit: Annotated[int, Query()] = 10,
):
    posts = await poster.read_many(author_id, limit, offset)
    if not posts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='No posts with given conditions found',
        ) from None
    return posts


@posts_router.get('/{post_id}/')
async def read_post(
    current_user: Annotated[User, Depends(get_current_user_stub)],
    poster: Annotated[PosterStub, Depends(poster_stub)],
    post_id: int,
):
    try:
        post = await poster.read_one(post_id)
    except PosterNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    return post


@posts_router.patch('/{post_id}/', response_model=Post)
async def update_post(
    current_user: Annotated[User, Depends(get_current_user_stub)],
    poster: Annotated[PosterStub, Depends(poster_stub)],
    post_id: int,
    body: PostUpdateRequest,
):
    try:
        post = await poster.patch(post_id, body.title, body.text)
    except PosterNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)
        ) from exc
    return post


@posts_router.delete('/{post_id}/', response_model=Post)
async def delete_post(
    current_user: Annotated[User, Depends(get_current_user_stub)],
    poster: Annotated[PosterStub, Depends(poster_stub)],
    post_id: int,
):
    try:
        post = await poster.delete(post_id)
    except PosterNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    return post


@posts_router.post('/{post_id}/like/', response_model=PostReactions)
async def like_post(
    current_user: Annotated[User, Depends(get_current_user_stub)],
    poster: Annotated[PosterStub, Depends(poster_stub)],
    post_id: int,
):
    try:
        response = await poster.react(post_id, current_user.id, True)
    except PosterPermissionError as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=str(exc)
        ) from exc
    except PosterNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)
        ) from exc
    return response


@posts_router.post('/{post_id}/dislike/', response_model=PostReactions)
async def dislike_post(
    current_user: Annotated[User, Depends(get_current_user_stub)],
    poster: Annotated[PosterStub, Depends(poster_stub)],
    post_id: int,
):
    try:
        response = await poster.react(post_id, current_user.id, False)
    except PosterPermissionError as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=str(exc)
        ) from exc
    except PosterNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)
        ) from exc
    return response
