from http import HTTPStatus
import pytest

@pytest.mark.asyncio
async def test_tasks_create_task_success(client, test_add_task): 

    user = test_add_task['user']
    project = test_add_task['project']
    column = test_add_task['column']

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
        f"/projects/{project.id}/board/columns/{column.id}/tasks",
        json = {
            "title": "TestTask",
            "description": None,
            "priority": "medium",
            "assignee_id": None
        }
    )

    assert response.status_code == HTTPStatus.CREATED

    data = response.json()

    assert data['title'] == 'TestTask'
    assert data['assignee_id'] is None

@pytest.mark.asyncio
async def test_tasks_create_task_unauthorized(client, test_add_task):

    project = test_add_task['project']
    column = test_add_task['column'] 

    response = await client.post(
        f"/projects/{project.id}/board/columns/{column.id}/tasks",
        json = {
            "title": "TestTask",
            "description": None,
            "prior`ity": "medium",
            "assignee_id": None
        }
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED

@pytest.mark.asyncio
async def test_tasks_get_tasks_success(client, test_tasks_for_user, test_user, test_project, test_column):
 
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
        f"/projects/{test_project.id}/board/columns/{test_column.id}/tasks"
    )

    assert response.status_code == HTTPStatus.OK

    data = response.json()

    assert isinstance(data, list)

    for i in range(10):
        assert data[i]['title'] == test_tasks_for_user[i].title

@pytest.mark.asyncio
async def test_tasks_get_tasks_unauthorized(client, test_column, test_project): 

    response = await client.get(
        f"/projects/{test_project.id}/board/columns/{test_column.id}/tasks"
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED

@pytest.mark.asyncio
async def test_tasks_get_task_success(client, test_user, test_project, test_column, test_task): 

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
        f"/projects/{test_project.id}/board/columns/{test_column.id}/tasks/{test_task.id}"
    )

    assert response.status_code == HTTPStatus.OK

    data = response.json()

    assert data['id'] == test_task.id
    assert data['title'] == test_task.title


@pytest.mark.asyncio
async def test_tasks_get_task_unauthorized(client, test_project, test_column, test_task): 

    response = await client.get(
        f"/projects/{test_project.id}/board/columns/{test_column.id}/tasks/{test_task.id}"
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED

@pytest.mark.asyncio
async def test_tasks_change_task_success(client, test_user, test_project, test_column, test_task): 

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
        f"/projects/{test_project.id}/board/columns/{test_column.id}/tasks/{test_task.id}",
        json = {
            "title": "TestTaskMe"
        }
    )

    assert response.status_code == HTTPStatus.OK

    data = response.json()

    assert data['title'] == "TestTaskMe"

@pytest.mark.asyncio
async def test_tasks_change_task_unauthorized(client, test_project, test_column, test_task): 

    response = await client.patch(
        f"/projects/{test_project.id}/board/columns/{test_column.id}/tasks/{test_task.id}",
        json = {
            "title": "TestTaskMe"
        }
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED

@pytest.mark.asyncio
async def test_tasks_delete_task_success(client, test_user, test_project, test_column, test_task): 


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
        f"/projects/{test_project.id}/board/columns/{test_column.id}/tasks/{test_task.id}",
    )

    assert response.status_code == HTTPStatus.NO_CONTENT


@pytest.mark.asyncio
async def test_tasks_delete_task_unauthorized(client, test_project, test_column, test_task): 

    response = await client.delete(
        f"/projects/{test_project.id}/board/columns/{test_column.id}/tasks/{test_task.id}",
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED