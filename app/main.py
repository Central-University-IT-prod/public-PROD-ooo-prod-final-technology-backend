from contextlib import asynccontextmanager

from fastapi import FastAPI

from core.config import config
from api.v1.routes import routers as v1_router
from core.database import engine


@asynccontextmanager
async def lifespan(_: FastAPI):
    from sqlalchemy import text
    async with engine.connect() as con:
        with open("../database-init.sql") as file:
            try:
                query = text(file.read())
                await con.execute(query)
                await con.commit()
            except:
                print('Skills table already filled')
    yield


app = FastAPI(
    title=config.PROJECT_NAME,
    version='1.0.0',
    lifespan=lifespan,
)

app.include_router(v1_router)


@app.get('/ping')
async def ping():
    return {"ping": "pong"}
