
import pytest
from httpx import ASGITransport, AsyncClient
from app.main import app
import config
BASE_URL = f"http://{config.HOST}:{config.PORT}"


@pytest.mark.anyio
async def test_index():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url=BASE_URL
    ) as aclient:
        response = await aclient.get("/")
    print('response.text ',response.text)
    assert response.status_code == 200
    assert response.text == response.text == '"ok"'

