from fastapi import FastAPI, APIRouter
from contextlib import asynccontextmanager

from app.database.database import create_tables, delete_tables
from app.api.handlers.users import router as user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await delete_tables()
    await create_tables()
    yield


def setup_handlers(*args) -> None:
    main_router = APIRouter(
        prefix='/api/v1/bse',
    )
    for router in args:
        main_router.include_router(router)

    return main_router


app = FastAPI(
    title='bse',
    lifespan=lifespan,
)
app.include_router(
    setup_handlers(
        user_router,
    )
)