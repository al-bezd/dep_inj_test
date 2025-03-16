

from db.controller import DBSessionDep
from db.models.item import Item
from fastapi import APIRouter
from view.models.item import ItemView

router = APIRouter()


@router.get("/items/", tags=["items"], response_model=ItemView)
async def read_users(session: DBSessionDep, name: str, description: str) -> ItemView:
    kwarg = {
        'name': name,
        'description': description
    }
    is_ext_obj = await Item.is_exist(session, kwarg['name'])
    if is_ext_obj:
        await session.refresh(is_ext_obj, list(Item.__annotations__.keys()))
        for key, value in kwarg.items():
            setattr(is_ext_obj, key, value)
        await Item.save(session, is_ext_obj)
        view_model = await is_ext_obj.out()
        print("Call index update ", kwarg, view_model, is_ext_obj)
        return view_model

    item = Item()
    for key, value in kwarg.items():
        setattr(item, key, value)
    await Item.save(session, item)
    print("Call index save ", kwarg)
    view_model = await item.out()
    return view_model
