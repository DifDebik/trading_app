from typing import AsyncGenerator

from fastapi import Depends
from fastapi_users.db import SQLAlchemyUserDatabase, SQLAlchemyBaseUserTable
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, declarative_base, mapped_column, Mapped
from sqlalchemy import String, Boolean, Integer, TIMESTAMP, ForeignKey
from datetime import datetime, timezone

from models.models import role
from config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER


DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
Base: DeclarativeBase = declarative_base()


class User(SQLAlchemyBaseUserTable[int], Base):
    id: Mapped[str] = mapped_column(
        Integer, primary_key=True
        )
    username: Mapped[str] = mapped_column(
        String, nullable=False
        )
    registered_at: Mapped[str] = mapped_column(
        TIMESTAMP(timezone=True), default=datetime.now(timezone.utc)
        )
    role_id: Mapped[str] = mapped_column(
        Integer, ForeignKey(role.c.id)
        )
    email: Mapped[str] = mapped_column(
        String(length=320), unique=True, index=True, nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(
        String(length=1024), nullable=False
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    is_verified: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )


engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)
