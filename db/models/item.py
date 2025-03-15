from sqlalchemy import String, select
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
# from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from db.models.base import Base
from view.models.item import ItemView


class Item(Base):
    __tablename__ = "item"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(128))
    description: Mapped[str] = mapped_column(
        String(), nullable=True, default='')

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id!r}, name={self.name!r}, description={self.description!r})"

    @staticmethod
    async def save(session: AsyncSession, item):
        if item.id is None:
            session.add(item)
        await session.commit()

    @staticmethod
    async def is_exist(session: AsyncSession, name: str):
        """Проверяет, существует ли запись с таким URL в базе данных."""
        query = select(Item).where(Item.name == name)
        res = await session.execute(query)
        res = res.scalars().all()
        if len(res) > 0:
            return res[0]
        return None

    async def out(self):
        return ItemView(
            id=await self.awaitable_attrs.id, 
            name=await self.awaitable_attrs.name, 
            description=await self.awaitable_attrs.description
        )
