from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from auth.base_config import auth_backend, fastapi_users
from auth.schemas import UserCreate, UserRead
from operations.router import router as router_operation
from pages.router import router as router_pages
from tasks.router import router as router_tasks
from chat.router import router as router_chat


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    redis = aioredis.from_url("redis://localhost")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield

app = FastAPI(
    title="Trading App",
    lifespan=lifespan,
)

app.mount('/static', StaticFiles(directory='static'), name='static')

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(router_tasks)
app.include_router(router_operation)
app.include_router(router_pages)
app.include_router(router_chat)

origins = [
    "http://localhost",
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['GET', 'POST', 'PUT', 'PATCH', 'OPTIONS', 'DELETE'],
    allow_headers=["Content-Type", "Set-Cookie",
                   "Access-Control-Allow-Headers",
                   "Access-Control-Allow-Origin"],
)
