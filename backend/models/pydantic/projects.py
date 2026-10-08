from pydantic import BaseModel

class CreateProject(BaseModel):
    name: str
    description: str | None = None

class SchemaProject(BaseModel):
    id: int 
    name: str
    description: str | None
    owner_id: int

class ResponseProject(SchemaProject): pass


class UpdateProject(BaseModel):
    name: str | None = None
    description: str | None = None
    