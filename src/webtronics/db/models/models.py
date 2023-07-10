"""Declarative base module."""
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):  # pylint: disable=too-few-public-methods
    """Declarative base class"""


class User(Base):  # pylint: disable=too-few-public-methods
    """User schema"""

    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    username: Mapped[str] = mapped_column()
    password: Mapped[str] = mapped_column()
    reactions: Mapped[list['Reaction']] = relationship(back_populates='user')


class Post(Base):
    """Post schema"""

    __tablename__ = 'posts'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column()
    text: Mapped[str] = mapped_column()
    author_id: Mapped[int] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE'), nullable=False
    )
    author: Mapped['User'] = relationship()
    reactions: Mapped[list['Reaction']] = relationship(back_populates='post')


class Reaction(Base):
    """Like/dislike table"""

    __tablename__ = 'reactions'

    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE'), primary_key=True
    )
    post_id: Mapped[int] = mapped_column(
        ForeignKey('posts.id', ondelete='CASCADE'), primary_key=True
    )
    like: Mapped[bool]
    user: Mapped['User'] = relationship(back_populates='reactions')
    post: Mapped['Post'] = relationship(back_populates='reactions')
