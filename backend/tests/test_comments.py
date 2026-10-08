from http import HTTPStatus
import pytest

@pytest.mark.asyncio
async def test_comments_add_comment_success(client, test_add_comment): 

    user = test_add_comment['user']
    project = test_add_comment['project']
    column = test_add_comment['column']
    task = test_add_comment['task']

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
        f'/projects/{project.id}/board/columns/{column.id}/tasks/{task.id}/comments',
        json = {
            "text": "i love you so much"
        }
    )

    assert response.status_code == HTTPStatus.CREATED

    data = response.json()

    assert data['text'] == 'i love you so much'

@pytest.mark.asyncio
async def test_comments_add_comment_unauthorized(client, test_add_comment): 

    project = test_add_comment['project']
    column = test_add_comment['column']
    task = test_add_comment['task']

    response = await client.post(
        f'/projects/{project.id}/board/columns/{column.id}/tasks/{task.id}/comments',
        json = {
            "text": "i love you so much"
        }
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED


@pytest.mark.asyncio
async def test_comments_get_comments_success(
    client, 
    test_user, 
    test_project, 
    test_column, 
    test_task, 
    test_comments_for_user
): 

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
        f'/projects/{test_project.id}/board/columns/{test_column.id}/tasks/{test_task.id}/comments'
    )

    assert response.status_code == HTTPStatus.OK

    data = response.json()

    assert isinstance(data, list)
    assert len(data) == 10

    for i in range(10):
        assert data[i]['text'] == test_comments_for_user[i].text

@pytest.mark.asyncio
async def test_comments_get_comments_unauthorized(client, test_project, test_column, test_task): 

    response = await client.get(
        f'/projects/{test_project.id}/board/columns/{test_column.id}/tasks/{test_task.id}/comments'
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED

@pytest.mark.asyncio
async def test_comments_get_comment_success(
    client, 
    test_user, 
    test_project, 
    test_column, 
    test_task, 
    test_comment
): 

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
        f'/projects/{test_project.id}/board/columns/{test_column.id}/tasks/{test_task.id}/comments/{test_comment.id}'
    )

    assert response.status_code == HTTPStatus.OK

    data = response.json()

    assert data['text'] == test_comment.text

@pytest.mark.asyncio
async def test_comments_get_comment_unauthorized(
    client, 
    test_project, 
    test_column, 
    test_task, 
    test_comment
):


    response = await client.get(
        f'/projects/{test_project.id}/board/columns/{test_column.id}/tasks/{test_task.id}/comments/{test_comment.id}'
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED

@pytest.mark.asyncio
async def test_comments_update_comment_success(
    client, 
    test_user,
    test_project, 
    test_column, 
    test_task, 
    test_comment
):

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
        f'/projects/{test_project.id}/board/columns/{test_column.id}/tasks/{test_task.id}/comments/{test_comment.id}',
        json = {
            "text": "Hello, World!"
        }
    )

    assert response.status_code == HTTPStatus.OK

    data = response.json()

    assert data['text'] == 'Hello, World!'

@pytest.mark.asyncio
async def test_comments_update_comment_unauthorized(
    client, 
    test_project, 
    test_column, 
    test_task, 
    test_comment
):

    response = await client.patch(
        f'/projects/{test_project.id}/board/columns/{test_column.id}/tasks/{test_task.id}/comments/{test_comment.id}',
        json = {
            "text": "Hello, asdf!"
        }
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED

@pytest.mark.asyncio
async def test_comments_delete_comment_success(
    client, 
    test_user,
    test_project, 
    test_column, 
    test_task, 
    test_comment
): 

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
        f'/projects/{test_project.id}/board/columns/{test_column.id}/tasks/{test_task.id}/comments/{test_comment.id}',
    )

    assert response.status_code == HTTPStatus.NO_CONTENT

@pytest.mark.asyncio
async def test_comments_delete_comment_unauthorized(
    client, 
    test_project, 
    test_column, 
    test_task, 
    test_comment
): 

    response = await client.delete(
        f'/projects/{test_project.id}/board/columns/{test_column.id}/tasks/{test_task.id}/comments/{test_comment.id}',
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED