# main.py

from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends

from auth import verify_api_key
from db.oracle import init_pool, close_pool
from controllers.student_controller import router as student_router
from controllers.search_controller import router as search_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Open the Oracle pool once, here, instead of at module-import time.
    init_pool()
    yield
    close_pool()


app = FastAPI(dependencies=[Depends(verify_api_key)], lifespan=lifespan)

app.include_router(student_router)
app.include_router(search_router)
