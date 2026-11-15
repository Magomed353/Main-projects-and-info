from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import  Session, sessionmaker
from sqlalchemy import URL, create_engine, text, insert, select
from .config import setting
from .model import Base , User, Task
import asyncio 

engine = create_async_engine(url=setting.DATABASE_URL, echo=True)#, pool_size=5, max_overflow=1
Session = sessionmaker(engine)


async def drop_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def create_user(user):
    async with engine.begin() as conn:
        await conn.execute(insert(User).values(login=user.login, password=user.password_hash))

async def get_hash_db(login):
    async with AsyncSession(engine) as conn:
        statement = select(User.password).filter_by(login=login)
        result = await conn.execute(statement)
        return result.scalar_one_or_none()

async def get_login_db(login):
    async with AsyncSession(engine) as conn:
        statement = select(User.login).filter_by(login=login)
        result = await conn.execute(statement)
        return result.scalar_one_or_none()

async def delete_task(user):
    async with engine.begin() as conn:
        pass
async def patch_task(user):
    async with engine.begin() as conn:
        pass
