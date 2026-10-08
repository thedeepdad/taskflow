from pydantic import BaseModel

class SchemaColumn(BaseModel):
    title: str

class CreateColumn(SchemaColumn): pass

class ResponseColumn(SchemaColumn): pass

class UpdateColumn(BaseModel): 
    title: str | None = None
    

