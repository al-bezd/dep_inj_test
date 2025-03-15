import asyncio
from db.controller import get_db_session
from db.models.item import Item


async def index(**kwarg):
    session = await anext(get_db_session())
    try:
        # Получаем первое значение
        is_ext_obj = await Item.is_exist(session, kwarg['id'])
        if is_ext_obj:
            await session.refresh(is_ext_obj, list(Item.__annotations__.keys()))
            for key, value in kwarg.items():
                setattr(is_ext_obj,key,value)
            await Item.save(session, is_ext_obj)
            view_model = await is_ext_obj.out()
            print("Call index update ", kwarg, view_model, is_ext_obj)
            return
        item = Item(name=kwarg['id'])
        await Item.save(session, item)
        print("Call index save ", kwarg)
    finally:
        await session.close() 



async def main():
    await index(id=1, description=f'hello world 1 v{VERSION}')
    tasks = [index(id=2, description=f'hello world 2 v{VERSION}'),
             index(id=3, description=f'hello world 3 v{VERSION}')]
    await asyncio.gather(*tasks)

VERSION = "3"
if __name__ == "__main__":
    asyncio.run(main())
    # print(Base.metadata.tables)
