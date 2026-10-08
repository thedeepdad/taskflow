from http import HTTPStatus
from sqlalchemy import select
from models import User
import pytest


# --------Test-Login--------


@pytest.mark.asyncio
async def test_login_success(client, test_user): 
    response = await client.post(
        "/auth/login",
        data = {
            "username": test_user.username,
            "password": "password123"
        }
    )

    assert response.status_code == HTTPStatus.OK

    assert response.cookies.get('access_token')
    assert response.cookies.get('refresh_token')

@pytest.mark.asyncio
async def test_login_wrong_password(client, test_user): 
    response = await client.post(
        "/auth/login",
        data = {
            "username": test_user.username,
            "password": "wrong_password"
        }
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED

@pytest.mark.asyncio
async def test_login_wrong_username(client): 
    response = await client.post(
        "/auth/login",
        data = {
            "username": "wrong_username",
            "password": "password123"
        }
    )


    assert response.status_code == HTTPStatus.UNAUTHORIZED

@pytest.mark.asyncio
async def test_login_without_username(client): 
    response = await client.post(
        "/auth/login",
        data = {
            "password": "password123"
        }
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

@pytest.mark.asyncio
async def test_login_without_password(client):
    response = await client.post(
        "/auth/login",
        data = {
            "username": "test_user"
        }
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


# --------Test-Register--------


@pytest.mark.asyncio
async def test_register_success(client, session):
    response = await client.post(
        "/auth/register",
        data={
            "username": "new_user",
            "email": "new_user@example.com",
            "password": "password123",
        },
    )

    assert response.status_code == HTTPStatus.CREATED

    user = await session.scalar(\
        select(User).where(User.username == 'new_user')
    )

    assert user is not None

    await session.delete(user)
    await session.commit()

@pytest.mark.asyncio
async def test_register_duplicate_username(client, test_user):
    response = await client.post(
        "/auth/register",
        data = {
            "username": 'test_user',
            "email": "123@example.com",
            "password": "password123"       
        }
    )

    assert response.status_code == HTTPStatus.CONFLICT

@pytest.mark.asyncio
async def test_register_duplicate_email(client, test_user):
    response = await client.post(
        "/auth/register",
        data = {
            "username": "another_user",
            "email": 'test_user1@example.com',
            "password": "password123"
        }
    )

    assert response.status_code == HTTPStatus.CONFLICT

@pytest.mark.asyncio
async def test_register_without_username(client): 
    response = await client.post(
        "/auth/register",
        data = {
            "password": "password123",
            "email": "another@example.com"
        }
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

# --------Test-Refresh--------

@pytest.mark.asyncio
async def test_refresh_success(client, test_user): 
    login_response = await client.post(
        "/auth/login",
        data = {
            "username": test_user.username,
            "password": "password123"
        }
    )

    assert login_response.status_code == HTTPStatus.OK

    response = await client.post("/auth/refresh")

    assert response.status_code == HTTPStatus.NO_CONTENT
    assert response.cookies.get('access_token')
    assert response.cookies.get('refresh_token')

@pytest.mark.asyncio
async def test_refresh_without_token(client): 
    response = await client.post(
        "/auth/refresh"
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED

@pytest.mark.asyncio
async def test_refresh_with_invalid_token(client): 
    client.cookies.set(
        "refresh_token", 
        "invalid_refresh_token"
    )

    response = await client.post(
        "/auth/refresh"
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED

@pytest.mark.asyncio
async def test_refresh_after_logout(client, test_user): 
    response = await client.post(
        "/auth/login",
        data = {
            "username": test_user.username,
            "password": "password123"
        }
    )

    assert response.status_code == HTTPStatus.OK
    assert response.cookies.get("refresh_token")
    assert response.cookies.get("access_token")

    logout_response = await client.post("/auth/logout")
    assert logout_response.status_code == HTTPStatus.NO_CONTENT

    response = await client.post("/auth/refresh")

    assert response.status_code == HTTPStatus.UNAUTHORIZED

# --------Test-LogOut--------

@pytest.mark.asyncio
async def test_logout_success(client, test_user): 
    login_response = await client.post(
        "/auth/login",
        data = {
            "username": test_user.username,
            "password": "password123"
        }
    )

    assert login_response.status_code == HTTPStatus.OK
    assert login_response.cookies.get("refresh_token")
    assert login_response.cookies.get("access_token")

    logout_response = await client.post("/auth/logout")

    assert logout_response.status_code == HTTPStatus.NO_CONTENT


@pytest.mark.asyncio
async def test_logout_without_auth(client): 

    response = await client.post("/auth/logout")

    assert response.status_code == HTTPStatus.NO_CONTENT

@pytest.mark.asyncio
async def test_logout_delete_cookies(client, test_user): 
    login_response = await client.post(
        "/auth/login",
        data = {
            "username": test_user.username,
            "password": "password123"     
        }
    )

    assert login_response.status_code == HTTPStatus.OK

    logout_response = await client.post("/auth/logout")

    assert logout_response.status_code == HTTPStatus.NO_CONTENT

    assert logout_response.cookies.get("refresh_token") is None
    assert logout_response.cookies.get("access_token") is None

# --------Test-GetMe--------

@pytest.mark.asyncio
async def test_get_me_success(client, test_user): 
    login_response = await client.post(
        "/auth/login",
        data = {
            "username": test_user.username,
            "password": "password123"
        }
    )

    assert login_response.status_code == HTTPStatus.OK

    response = await client.get("/auth/me")

    assert response.status_code == HTTPStatus.OK

    data = response.json()

    assert data["id"] == test_user.id
    assert data["username"] == test_user.username
    assert data["email"] == test_user.email

@pytest.mark.asyncio
async def test_get_me_unauthorized(client): 
    response = await client.get("/auth/me")

    assert response.status_code == HTTPStatus.UNAUTHORIZED\

    