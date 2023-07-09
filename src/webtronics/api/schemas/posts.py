from pydantic import BaseModel

from webtronics.api.schemas.users import User


class PostCreateRequest(BaseModel):
    title: str
    text: str


class PostDTO(BaseModel):
    id: int
    title: str
    text: str
    author_id: int
    author: User


class Post(BaseModel):
    id: int
    title: str
    text: str
    author: User


class PostUpdateRequest(BaseModel):
    title: str | None = None
    text: str | None = None


class PostReactions(BaseModel):
    post_id: int
    likes: int
    dislikes: int
