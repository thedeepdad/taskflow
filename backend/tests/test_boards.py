from http import HTTPStatus
import pytest

@pytest.mark.asyncio
async def test_boards_add_board_success(client, test_add_board): 

    user = test_add_board['user']
    project = test_add_board['project']

    response_login = await client.post(
        "/auth/login",
        data = {
            "username": user.username,
            "password": "password123"
        }
    )

    assert response_login.status_code == HTTPStatus.OK
    assert response_login.cookies.get("refresh_token")
    assert response_login.cookies.get("access_token")


    response = await client.post(
        f"/projects/{project.id}/board",
        json = {
            "name": "TestBoard"
        }
    )

    assert response.status_code == HTTPStatus.CREATED

    data = response.json()

    assert data["name"] == "TestBoard"

@pytest.mark.asyncio
async def test_boards_add_board_unauthorized(client, test_add_board): 

    project = test_add_board['project']

    response = await client.post(
        f"/projects/{project.id}/board",
        json = {
            "name": "TestBoard"
        }
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED

@pytest.mark.asyncio
async def test_boards_get_board_success(client, test_user, test_project, test_board): 

    response_login = await client.post(
        "/auth/login",
        data = {
            "username": test_user.username,
            "password": "password123"
        }
    )

    assert response_login.status_code == HTTPStatus.OK
    assert response_login.cookies.get("refresh_token")
    assert response_login.cookies.get("access_token")


    response = await client.get(
        f"/projects/{test_project.id}/board",
    )

    assert response.status_code == HTTPStatus.OK

    data = response.json()

    assert len(data) == 1
    assert data['name'] == test_board.name

@pytest.mark.asyncio
async def test_boards_get_board_unauthorized(client, test_project): 


    response = await client.get(
        f"/projects/{test_project.id}/board",
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED

@pytest.mark.asyncio
async def test_boards_update_board_success(client, test_user, test_project, test_board): 

    response_login = await client.post(
        "/auth/login",
        data = {
            "username": test_user.username,
            "password": "password123"
        }
    )

    assert response_login.status_code == HTTPStatus.OK
    assert response_login.cookies.get("refresh_token")
    assert response_login.cookies.get("access_token")

    response = await client.patch(
        f"/projects/{test_project.id}/board",
        json = {
            "name": "JustBoard"
        }
    )

    assert response.status_code == HTTPStatus.OK

    data = response.json()

    assert data['name'] == "JustBoard"

@pytest.mark.asyncio
async def test_boards_update_board_unauthorized(client, test_project, test_board): 

    response = await client.patch(
        f"/projects/{test_project.id}/board",
        json = {
            "name": "JustBoard"
        }
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED

@pytest.mark.asyncio
async def test_boards_delete_board_success(client, test_user, test_project, test_board): 

    response_login = await client.post(
        "/auth/login",
        data = {
            "username": test_user.username,
            "password": "password123"
        }
    )

    assert response_login.status_code == HTTPStatus.OK
    assert response_login.cookies.get("refresh_token")
    assert response_login.cookies.get("access_token")

    response = await client.delete(
        f"/projects/{test_project.id}/board"
    )

    assert response.status_code == HTTPStatus.NO_CONTENT

@pytest.mark.asyncio
async def test_boards_delete_board_unauthorized(client, test_project, test_board): 

    response = await client.delete(
        f"/projects/{test_project.id}/board"
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
