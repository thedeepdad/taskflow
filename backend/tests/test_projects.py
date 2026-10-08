from http import HTTPStatus
import pytest

@pytest.mark.asyncio
async def test_projects_add_project_success(client, test_add_project): 
    response_login = await client.post(
        "/auth/login",
        data = {
            "username": test_add_project.username,
            "password": "password123"
        }
    )

    assert response_login.status_code == HTTPStatus.OK
    assert response_login.cookies.get("refresh_token")
    assert response_login.cookies.get("access_token") 

    response = await client.post(
        "/projects",
        json = {
            "name": "TestProject",
            "description": None,
        }
    )


    assert response.status_code == HTTPStatus.CREATED

    data = response.json()

    assert data["id"] is not None
    assert isinstance(data['id'], int)

    assert data['name'] == 'TestProject'
    assert data['description'] is None

    assert data['owner_id'] == test_add_project.id

@pytest.mark.asyncio
async def test_projects_add_project_unauthorized(client):

    response = await client.post(
        "/projects",
        json = {
            "name": "TestProject",
            "description": None,
        }
    )


    assert response.status_code == HTTPStatus.UNAUTHORIZED

@pytest.mark.asyncio
async def test_projects_get_projects_success(client, test_user, test_proejcts_for_user): 
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

    response = await client.get('/projects')

    assert response.status_code == HTTPStatus.OK

    projects = response.json()

    assert isinstance(projects, list)
    assert len(projects) > 1

    assert projects[0]['id'] == test_proejcts_for_user[0].id
    assert projects[0]['name'] == test_proejcts_for_user[0].name

@pytest.mark.asyncio
async def test_projects_get_projects_unauthorized(client): 
    response = await client.get('/projects')

    assert response.status_code == HTTPStatus.UNAUTHORIZED

@pytest.mark.asyncio
async def test_projects_get_project_success(client, test_user, test_project): 
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

    response = await client.get(f'/projects/{project.id}')

    assert response.status_code == HTTPStatus.OK

    data = response.json()

    assert data['id'] == project.id
    assert data['name'] == project.name

@pytest.mark.asyncio
async def test_projects_get_project_unauthorized(client, test_project): 

    project = test_project

    response = await client.get(f'/projects/{project.id}')

    assert response.status_code == HTTPStatus.UNAUTHORIZED

@pytest.mark.asyncio
async def test_projects_update_project_success(client, test_user, test_project): 
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

    response = await client.patch(
        f"/projects/{project.id}",
        json = {
            "name": "Project",
            "description": None
        }
    )

    assert response.status_code == HTTPStatus.OK

    data = response.json()

    assert data["id"] == test_project.id
    assert data["name"] == "Project"

@pytest.mark.asyncio
async def test_projects_update_project_unauthorized(client, test_project): 

    project = test_project

    response = await client.patch(
        f"/projects/{project.id}",
        json = {
            "name": "Project",
            "description": None
        }
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED

@pytest.mark.asyncio
async def test_projects_delete_project_success(client, test_project, test_user): 
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

    response = await client.delete(f"/projects/{project.id}")

    assert response.status_code == HTTPStatus.NO_CONTENT

@pytest.mark.asyncio
async def test_projects_delete_project_unauthorized(client, test_project):

    project = test_project

    response = await client.delete(f"/projects/{project.id}")

    assert response.status_code == HTTPStatus.UNAUTHORIZED

@pytest.mark.asyncio
async def test_projects_get_members_success(client, test_user, test_project): 

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

    response = await client.get(f"/projects/{project.id}/members")

    assert response.status_code == HTTPStatus.OK

    data = response.json()

    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]['username'] == test_user.username
    assert data[0]['email'] == test_user.email
    assert data[0]['role'] == test_user.role

@pytest.mark.asyncio
async def test_projects_get_members_unauthorized(client, test_project): 

    project = test_project

    response = await client.get(f"/projects/{project.id}/members")

    assert response.status_code == HTTPStatus.UNAUTHORIZED

@pytest.mark.asyncio
async def test_projects_add_member_success(client, test_user, test_project, test_member): 

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

    response = await client.post(
        f"/projects/{project.id}/members",
        json = {
            "username": test_member.username,
            "role": "member"
        }
    )

    assert response.status_code == HTTPStatus.CREATED

@pytest.mark.asyncio
async def test_projects_add_member_unauthorized(client, test_project, test_member): 

    project = test_project

    response = await client.post(
        f"/projects/{project.id}/members",
        json = {
            "username": test_member.username,
            "role": "member"
        }
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED

@pytest.mark.asyncio
async def test_projects_change_member_success(client, test_user, test_project, test_member): 

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

    response_project = await client.post(
        f"/projects/{project.id}/members",
        json = {
            "username": test_member.username,
            "role": "member"
        }
    )

    assert response_project.status_code == HTTPStatus.CREATED


    response = await client.patch(
        f'/projects/{project.id}/members/{test_member.id}',
        json = {
            "role": "manager"
        }
    )

    assert response.status_code == HTTPStatus.OK

    data = response.json()

    assert data["role"] == "manager"

@pytest.mark.asyncio
async def test_projects_change_member_unauthorized(client, test_project, test_member): 

    project = test_project

    response = await client.patch(
        f"/projects/{project.id}/members/{test_member.id}",
        json = {
            "role": "manager"
        }
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED

@pytest.mark.asyncio
async def test_projects_delete_member_success(client, test_user, test_project, test_member): 

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

    response_project = await client.post(
        f"/projects/{project.id}/members",
        json = {
            "username": test_member.username,
            "role": "member"
        }
    )

    assert response_project.status_code == HTTPStatus.CREATED

    response = await client.delete(f"/projects/{project.id}/members/{test_member.id}")

    assert response.status_code == HTTPStatus.NO_CONTENT

@pytest.mark.asyncio
async def test_proejects_delete_member_unauthorized(client, test_project, test_member): 

    project = test_project

    response = await client.delete(f"/projects/{project.id}/members/{test_member.id}")

    assert response.status_code == HTTPStatus.UNAUTHORIZED

