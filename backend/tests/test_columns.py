from http import HTTPStatus
import pytest

@pytest.mark.asyncio
async def test_columns_add_column_success(client, test_add_column): 

    user = test_add_column['user']
    project = test_add_column['project']

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
        f"/projects/{project.id}/board/columns",
        json={
            "title": "In Progress"
        }
    )

    assert response.status_code == HTTPStatus.CREATED

    data = response.json()

    assert data['title'] == "In Progress"

@pytest.mark.asyncio
async def test_columns_add_column_unauthorized(client, test_add_column): 

    project = test_add_column['project']

    response = await client.post(
        f"/projects/{project.id}/board/columns",
        json = {
            "title": "In Progress",
        }
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED

@pytest.mark.asyncio
async def test_columns_get_columns_success(client, test_user, test_columns_for_users, test_project): 

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

    project = test_project

    response = await client.get(
        f"/projects/{project.id}/board/columns"
    )

    assert response.status_code == HTTPStatus.OK

    data = response.json()

    assert isinstance(data, list)
    assert len(data) == 10

    for i in range(10): 
        assert data[i]['title'] == test_columns_for_users[i].title

@pytest.mark.asyncio
async def test_columns_get_columns_unauthorized(client, test_project): 

    project = test_project

    response = await client.get(
        f"/projects/{project.id}/board/columns"
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED

@pytest.mark.asyncio
async def test_columns_get_column_success(client, test_user, test_column, test_project): 

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

    project = test_project
    column = test_column

    response = await client.get(
        f"/projects/{project.id}/board/columns/{column.id}"
    )

    assert response.status_code == HTTPStatus.OK

    data = response.json()

    assert data['title'] == column.title

@pytest.mark.asyncio
async def test_columns_get_column_unauthorized(client, test_project, test_column): 

    project = test_project
    column = test_column

    response = await client.get(
        f"/projects/{project.id}/board/columns/{column.id}"
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED

@pytest.mark.asyncio
async def test_columns_update_column_success(client, test_user, test_project, test_column): 
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

    project = test_project
    column = test_column

    response = await client.patch(
        f"/projects/{project.id}/board/columns/{column.id}",
        json = {
            "title": "Deleted"
        }
    )

    assert response.status_code == HTTPStatus.OK

    data = response.json()

    assert data["title"] == "Deleted"


@pytest.mark.asyncio
async def test_columns_update_column_unauthorized(client, test_project, test_column): 

    project = test_project
    column = test_column

    response = await client.patch(
        f"/projects/{project.id}/board/columns/{column.id}",
        json = {
            "title": "Deleted"
        }
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED

@pytest.mark.asyncio
async def test_columns_delete_column_success(client, test_user, test_project, test_column): 

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

    project = test_project
    column = test_column

    response = await client.delete(f"/projects/{project.id}/board/columns/{column.id}")

    assert response.status_code == HTTPStatus.NO_CONTENT

@pytest.mark.asyncio
async def test_columns_delete_column_unauthorized(client, test_project, test_column): 

    project = test_project
    column = test_column

    response = await client.delete(f"/projects/{project.id}/board/columns/{column.id}")

    assert response.status_code == HTTPStatus.UNAUTHORIZED