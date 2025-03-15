import contextlib
from sqlalchemy.orm import sessionmaker
import contextlib
import asyncio
from typing import Any, AsyncIterator, Annotated
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession, AsyncConnection
from sqlalchemy.orm import sessionmaker
#from fastapi import Depends
import config
# engine = create_engine(config.DATABASE_URL)
# SessionLocal = sessionmaker(engine)
echo = False
engine = create_async_engine(config.DATABASE_URL, echo=echo)
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

# def session_gen() -> Generator[Session]:
#     db = SessionLocal()
#     try:
#         print("сессия создана")
#         yield db
#     finally:
#         db.close()
#         print("сессия уничтожена")


class DatabaseSessionManager:
    def __init__(self, host: str, engine_kwargs: dict[str, Any] = {}):
        self._engine = create_async_engine(host, **engine_kwargs)
        self._sessionmaker = async_sessionmaker(autocommit=False, bind=self._engine)

    async def close(self):
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")
        await self._engine.dispose()

        self._engine = None
        self._sessionmaker = None

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")

        async with self._engine.begin() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self._sessionmaker is None:
            raise Exception("DatabaseSessionManager is not initialized")

        session = self._sessionmaker(
            #class_=AsyncSession
            #expire_on_commit=False
            )
        try:
            yield session
        except Exception:
            await session.rollback()
            await session.close()
            raise
        finally:
            pass
            #await session.close()

#asyncio.create_task(check_init_models())

sessionmanager = DatabaseSessionManager(config.DATABASE_URL, {"echo": echo})


async def get_db_session():
    async with sessionmanager.session() as session:
        yield session

#DBSessionDep = Annotated[AsyncSession, Depends(get_db_session)]