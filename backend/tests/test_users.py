from http import HTTPStatus
import pytest

@pytest.mark.asyncio
async def test_users_get_me_success(client, test_user): 
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

    response = await client.get("/users/me")

    assert response.status_code == HTTPStatus.OK

    data = response.json()

    assert data["username"] == test_user.username
    assert data["email"] == test_user.email


@pytest.mark.asyncio
async def test_users_get_me_unauthorized(client, test_user): 

    response = await client.get("/users/me")

    assert response.status_code == HTTPStatus.UNAUTHORIZED

@pytest.mark.asyncio
async def test_users_change_me_success(client, test_user): 
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
        "/users/me",
        json = {
            "username": "new_username"
        }
    )


    assert response.status_code == HTTPStatus.OK

    data = response.json()

    assert data["username"] == "new_username"
    assert data["email"] == test_user.email


@pytest.mark.asyncio
async def test_users_change_me_unauthorized(client): 

    response = await client.patch(
        "/users/me",
        json = {
            "username": "new_username"
        }
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED

@pytest.mark.asyncio
async def test_users_delete_me_success(client, test_user_without_delete): 
    response_login = await client.post(
        "/auth/login",
        data = {
            "username": test_user_without_delete.username,
            "password": "password123"
        }
    )

    assert response_login.status_code == HTTPStatus.OK
    assert response_login.cookies.get("refresh_token")
    assert response_login.cookies.get("access_token")

    response = await client.delete(
        "/users/me"
    )

    assert response.status_code == HTTPStatus.NO_CONTENT


@pytest.mark.asyncio
async def test_users_delete_me_unauthorized(client): 
    response = await client.delete(
        "/users/me"
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED

@pytest.mark.asyncio
async def test_users_get_projects_me_success(
    client, 
    test_user,
    test_proejcts_for_user
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

    response = await client.get("/users/me/projects")

    assert response.status_code == HTTPStatus.OK

    data = response.json()

    assert len(data) == 10

    returned_names = {proejct["name"] for proejct in data}
    expected_names = {project.name for project in test_proejcts_for_user}

    assert returned_names == expected_names


@pytest.mark.asyncio
async def test_users_get_projects_me_unauthorized(client): 

    response = await client.get("/users/me/projects")

    assert response.status_code == HTTPStatus.UNAUTHORIZED

@pytest.mark.asyncio
async def test_users_get_tasks_success(
    client, 
    test_user, 
    test_tasks_for_user
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

    response = await client.get("/users/me/tasks")

    assert response.status_code == HTTPStatus.OK

    data = response.json()

    assert isinstance(data, list)
    assert len(data) == len(test_tasks_for_user)

    returned_ids = {task["id"] for task in data}
    expected_ids = {task.id for task in test_tasks_for_user}

    assert returned_ids == expected_ids


@pytest.mark.asyncio
async def test_users_get_tasks_unauthorized(client): 

    response = await client.get("/users/me/tasks")

    assert response.status_code == HTTPStatus.UNAUTHORIZED

@pytest.mark.asyncio
async def test_users_admin_success(client, test_admin): 
    response_login = await client.post(
        "/auth/login",
        data = {
            "username": test_admin.username,
            "password": "password123"
        }
    )

    assert response_login.status_code == HTTPStatus.OK
    assert response_login.cookies.get("refresh_token")
    assert response_login.cookies.get("access_token")  

    response = await client.get("/users")

    assert response.status_code == HTTPStatus.OK


@pytest.mark.asyncio
async def test_users_admin_forbidden(client, test_manager): 
    response_login = await client.post(
        "/auth/login",
        data = {
            "username": test_manager.username,
            "password": "password123"
        }
    )

    assert response_login.status_code == HTTPStatus.OK
    assert response_login.cookies.get("refresh_token")
    assert response_login.cookies.get("access_token")  

    response = await client.get("/users")

    assert response.status_code == HTTPStatus.FORBIDDEN

@pytest.mark.asyncio
async def test_users_user_forbidden(client, test_member): 
    response_login = await client.post(
        "/auth/login",
        data = {
            "username": test_member.username,
            "password": "password123"
        }
    )

    assert response_login.status_code == HTTPStatus.OK
    assert response_login.cookies.get("refresh_token")
    assert response_login.cookies.get("access_token")  

    response = await client.get("/users")

    assert response.status_code == HTTPStatus.FORBIDDEN


@pytest.mark.asyncio
async def test_users_unauthorized(client): 

    response = await client.get("/users")

    assert response.status_code == HTTPStatus.UNAUTHORIZED

@pytest.mark.asyncio
async def test_users_get_user_success(client, test_admin, test_users_for_user): 
    response_login = await client.post(
        "/auth/login",
        data = {
            "username": test_admin.username,
            "password": "password123"
        }
    )

    assert response_login.status_code == HTTPStatus.OK
    assert response_login.cookies.get("refresh_token")
    assert response_login.cookies.get("access_token") 

    user = test_users_for_user[0]

    response = await client.get(f"/users/{user.id}")

    assert response.status_code == HTTPStatus.OK

    data = response.json()

    assert data['id'] == user.id
    assert data['username'] == user.username
    assert data['email'] == user.email

@pytest.mark.asyncio
async def test_users_get_user_unathorized(client, test_users_for_user): 

    user = test_users_for_user[0]

    response = await client.get(f"/users/{user.id}")

    assert response.status_code == HTTPStatus.UNAUTHORIZED

@pytest.mark.asyncio
async def test_users_update_user(client, test_admin, test_users_for_user): 
    response_login = await client.post(
        "/auth/login",
        data = {
            "username": test_admin.username,
            "password": "password123"
        }
    )

    assert response_login.status_code == HTTPStatus.OK
    assert response_login.cookies.get("refresh_token")
    assert response_login.cookies.get("access_token") 

    user = test_users_for_user[0]

    response = await client.patch(
        f"/users/{user.id}",
        json = {
            "role": "member"
        }
    )

    assert response.status_code == HTTPStatus.OK

    data = response.json()

    assert data['id'] == user.id
    assert data['username'] == user.username
    assert data['email'] == user.email

@pytest.mark.asyncio
async def test_users_update_user_unauthorized(client, test_users_for_user): 

    user = test_users_for_user[0]

    response = await client.patch(
        f"/users/{user.id}",
        json = {
            "role": "member"
        }
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED

@pytest.mark.asyncio
async def test_users_delete_user_success(client, test_admin, test_users_for_user): 
    response_login = await client.post(
        "/auth/login",
        data = {
            "username": test_admin.username,
            "password": "password123"
        }
    )

    assert response_login.status_code == HTTPStatus.OK
    assert response_login.cookies.get("refresh_token")
    assert response_login.cookies.get("access_token") 

    user = test_users_for_user[0]

    response = await client.delete(f"/users/{user.id}")

    assert response.status_code == HTTPStatus.NO_CONTENT

@pytest.mark.asyncio
async def test_users_delete_user_unauthorized(client, test_users_for_user): 
    user = test_users_for_user[0]

    response = await client.delete(f"/users/{user.id}")

    assert response.status_code == HTTPStatus.UNAUTHORIZED
