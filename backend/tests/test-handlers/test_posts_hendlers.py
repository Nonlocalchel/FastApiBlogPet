import pytest
from httpx import AsyncClient


@pytest.mark.asyncio(loop_scope="function")
async def test_get_posts(client: AsyncClient):
    response = await client.get("/api/v1/posts/")
    assert response.status_code == 200


@pytest.mark.asyncio(loop_scope="function")
async def test_get_post(client: AsyncClient):
    response = await client.get("/api/v1/posts/1")
    assert response.status_code == 404
