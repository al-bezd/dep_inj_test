import asyncio
import datetime
import pytest
from httpx import ASGITransport, AsyncClient
import trio
from app.main import app
import uuid
import config
BASE_URL = f"http://{config.HOST}:{config.PORT}"

# async def gather(*tasks):

#     async def collect(index, task, results):
#         task_func, *task_args = task
#         results[index] = await task_func(*task_args)

#     results = {}
#     async with trio.open_nursery() as nursery:
#         for index, task in enumerate(tasks):
#             nursery.start_soon(collect, index, task, results)
#     return [results[i] for i in range(len(tasks))]
# trio.gather = gather
# @pytest.mark.anyio()
# @pytest.mark.parametrize('anyio_backend', ['asyncio'])


@pytest.mark.asyncio
async def test_items():

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url=BASE_URL
    ) as aclient:
        tasks = [
            aclient.get('/items/', params={
                'name': 'name 1', 'description': f'hello world 1 v{uuid.uuid4().hex}/n{datetime.datetime.now()}'
            }),
            aclient.get('/items/', params={
                'name': 'name 2', 'description': f'hello world 2 v{uuid.uuid4().hex}/n{datetime.datetime.now()}'
            }),
            aclient.get('/items/', params={
                'name': 'name 3', 'description': f'hello world 3 v{uuid.uuid4().hex}/n{datetime.datetime.now()}'
            }),
        ]

        responses = await asyncio.gather(
            *tasks, return_exceptions=True
        )
        # responses = []
        # for task in tasks:
        #     response = await task
        #     responses.append(response)

        for response in responses:
            assert isinstance(
                response, Exception) or response.status_code == 200
