from db.controller import DBSessionDep
from fastapi import APIRouter

router = APIRouter()


@router.get('/')
async def index(session: DBSessionDep):
    return 'ok'
