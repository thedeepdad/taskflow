from enum import StrEnum

class Tags(StrEnum): 
    auth = 'auth'
    tasks = 'tasks'
    users = 'users'
    projects = 'projects'
    columns = 'columns'
    boards = 'boards'
    comments = 'comments'

class Prefix(StrEnum): 
    users = '/users'
    auth = '/auth'
    projects = '/projects'
    boards = '/projects/{project_id}/board'
    columns = '/projects/{project_id}/board/columns'
    tasks = '/projects/{project_id}/board/columns/{column_id}/tasks'
    comments = '/projects/{project_id}/board/columns/{column_id}/tasks/{task_id}/comments'

class UserRole(StrEnum): 
    member = 'member'
    manager = 'manger'
    admin = 'admin'

class TaskPriority(StrEnum): 
    low = 'low'
    medium = 'medium'
    high = 'high'