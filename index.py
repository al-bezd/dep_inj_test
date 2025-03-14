import asyncio
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

engine = create_engine("sqlite:///database.db")
SessionLocal = sessionmaker(engine)


def session_gen():
    db = SessionLocal()
    try:
        print("сессия создана")
        yield db
    finally:
        db.close()
        print("сессия уничтожена")


async def index(*arg, session: Session = session_gen()):
    session
    print("Call index ", arg)


async def main():
    await index(1)
    tasks = [index(2), index(3)]
    await asyncio.gather(tasks)


if __name__ == "__main__":
    asyncio.run(main())
