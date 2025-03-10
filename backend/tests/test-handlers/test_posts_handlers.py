import pytest
from httpx import AsyncClient


@pytest.mark.asyncio(loop_scope="function")
async def test_get_posts(client: AsyncClient):
    response = await client.get("/api/v1/posts/")
    assert response.status_code == 200
    assert len(response.json()) == 6


@pytest.mark.asyncio(loop_scope="function")
async def test_get_post_fail(client: AsyncClient, last_post: int):
    response = await client.get(f"/api/v1/posts/{last_post + 1}")
    assert response.status_code == 404


@pytest.mark.asyncio(loop_scope="function")
async def test_get_post_success(client: AsyncClient, last_post: int):
    response = await client.get(f"/api/v1/posts/{last_post}")
    assert response.status_code == 200


@pytest.mark.asyncio(loop_scope="function")
async def test_create_post(client: AsyncClient, auth_header: dict):
    post_data = {
        "title": "ss",
        "body": "ss"
    }
    response = await client.post("/api/v1/posts/", json=post_data, headers=auth_header)
    assert response.status_code == 201


@pytest.mark.asyncio(loop_scope="function")
async def test_update_post(client: AsyncClient, auth_header: dict, last_post: int):
    change_post_data = {
        "title": "ss",
        "body": ""
    }
    response = await client.patch(f"/api/v1/posts/{last_post}", json=change_post_data, headers=auth_header)
    assert response.status_code == 200
    new_post_response = await client.get(f"/api/v1/posts/{last_post}", headers=auth_header)
    new_post_data = new_post_response.json()
    assert new_post_data["title"] == change_post_data["title"]


@pytest.mark.asyncio(loop_scope="function")
async def test_update_post_fail(client: AsyncClient, auth_header: dict, last_post: int):
    change_post_data = {
        "title": "ss",
        "body": ""
    }
    response = await client.patch(f"/api/v1/posts/{last_post + 31}", json=change_post_data, headers=auth_header)
    assert response.status_code == 404


@pytest.mark.asyncio(loop_scope="function")
async def test_delete_post(client: AsyncClient, auth_header: dict, last_post: int):
    response = await client.delete(f"/api/v1/posts/{last_post}", headers=auth_header)
    assert response.status_code == 204


@pytest.mark.asyncio(loop_scope="function")
async def test_delete_post_fail(client: AsyncClient, auth_header: dict, last_post: int):
    response = await client.delete(f"/api/v1/posts/{last_post+11}", headers=auth_header)
    assert response.status_code == 404
