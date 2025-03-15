import asyncio

from db.controller import get_db_session
from sqlalchemy.ext.asyncio import AsyncSession
from db.models.item import Item


async def index(**kwarg):
    session = await anext(get_db_session())
    # Получаем первое значение
    is_ext_obj = await Item.is_exist(session, kwarg['id'])
    if is_ext_obj:
        await session.refresh(is_ext_obj, list(Item.__annotations__.keys()))
        for key, value in kwarg.items():
            setattr(is_ext_obj,key,value)
        #is_ext_obj.name = kwarg['id']
        #is_ext_obj.description = kwarg['description']
        await Item.save(session, is_ext_obj)
        view_model = await is_ext_obj.out()
        print("Call index update ", kwarg, view_model, is_ext_obj)
        return
    item = Item(name=kwarg['id'])
    await Item.save(session, item)
    print("Call index save ", kwarg)


async def main():
    await index(id=1, description=f'hello world 1 v{VERSION}')
    tasks = [index(id=2, description=f'hello world 2 v{VERSION}'),
             index(id=3, description=f'hello world 3 v{VERSION}')]
    await asyncio.gather(*tasks)

VERSION = "2"
if __name__ == "__main__":
    asyncio.run(main())
    # print(Base.metadata.tables)
