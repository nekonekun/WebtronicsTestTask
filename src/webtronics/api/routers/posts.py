"""Post-related routes"""
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from webtronics.api.schemas.posts import Post, PostCreateRequest, PostUpdateRequest
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
    author_id: Annotated[int, Query()] = None,
    offset: Annotated[int, Query()] = 0,
    limit: Annotated[int, Query()] = 10,
):
    posts = await poster.read_many(author_id, limit, offset)
    if not posts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'No posts with given conditions found',
        )
    return posts


@posts_router.get('/{post_id}/')
async def read_post(
    current_user: Annotated[User, Depends(get_current_user_stub)],
    poster: Annotated[PosterStub, Depends(poster_stub)],
    post_id: int,
):
    post = await poster.read_one(post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Post with id {post_id} does not exist',
        )
    return post


@posts_router.patch('/{post_id}/', response_model=Post)
async def update_post(
        current_user: Annotated[User, Depends(get_current_user_stub)],
        poster: Annotated[PosterStub, Depends(poster_stub)],
        post_id: int,
        body: PostUpdateRequest):
    post = await poster.patch(post_id, body.title, body.text)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Post with id {post_id} does not exist',
        )
    return post


@posts_router.delete('/{post_id}/', response_model=Post)
async def delete_post(
        current_user: Annotated[User, Depends(get_current_user_stub)],
        poster: Annotated[PosterStub, Depends(poster_stub)],
        post_id: int):
    post = await poster.delete(post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Post with id {post_id} does not exist',
        )
    return post


@posts_router.post('/{post_id}/like/')
async def like_post(post_id: int):
    pass


@posts_router.post('/{post_id}/dislike/')
async def dislike_post(post_id: int):
    pass
