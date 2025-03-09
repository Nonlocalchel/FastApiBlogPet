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


@pytest.mark.asyncio(loop_scope="function")
async def test_create_post(client: AsyncClient, auth_token: str):
    post_data = {
        "title": "ss",
        "body": "ss"
    }
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = await client.post("/api/v1/posts/", json=post_data, headers=headers)
    assert response.status_code == 201
