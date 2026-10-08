from fastapi import status, HTTPException

def user_not_found() -> HTTPException: 
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='User not found'
    )

def project_not_found() -> HTTPException: 
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='Project not found'
    )

def board_not_found() -> HTTPException: 
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='Board not found'
    )

def column_not_found() -> HTTPException: 
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='Column not found'
    )

def task_not_found() -> HTTPException: 
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='Task not found'
    )

def comment_not_found() -> HTTPException: 
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='Comment not found'
    )

def member_not_found() -> HTTPException: 
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='Member not found'
    )

def database_unvailable() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        detail='Database temporarily unavailable'
    )

def raise_forbidden() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail='Not enough permissions'
    )

def requier_project_access() -> HTTPException: 
    return HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail='Youd don`t have access to this project'
    )

def requier_member() -> HTTPException: 
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='User is not a member of this project'
    )
def requier_comment_owner() -> HTTPException: 
    return HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail='You are not the owner of this comment'
    )

def username_already_exists() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail='Username already exists'
    )

def email_already_exists() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail='Email already exists'
    )

def member_already_exists() -> HTTPException:
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail='Member already exists'
    )

def board_already_exists() -> HTTPException:
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail='Board already exists'
    )

def assignee_not_found() -> HTTPException:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='Assignee not found'
    )