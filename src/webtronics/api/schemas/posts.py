from pydantic import BaseModel, Field

from webtronics.api.schemas.users import User


class PostCreateRequest(BaseModel):
    title: str = Field(examples=['title'], description='Post title')
    text: str = Field(examples=['text'], description='Post text')


class PostDTO(BaseModel):
    id: int
    title: str
    text: str
    author_id: int
    author: User


class Post(BaseModel):
    id: int = Field(examples=[0], description='Post id')
    title: str = Field(examples=['title'], description='Post title')
    text: str = Field(examples=['text'], description='Post text')
    author: User = Field(description='Post author')


class PostUpdateRequest(BaseModel):
    title: str | None = Field(
        examples=['new title'], description='New post title'
    )
    text: str | None = Field(
        examples=['new text'], description='New post text'
    )


class PostReactions(BaseModel):
    post_id: int = Field(examples=[0], description='Post id')
    likes: list[int] = Field(
        examples=[[1, 2]], description='Users who liked this post'
    )
    dislikes: list[int] = Field(
        examples=[[3, 4]], description='Users who disliked this post'
    )
