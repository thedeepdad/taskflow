from pydantic import BaseModel

class SchemaBoard(BaseModel): 
    name: str

class CreateBoard(SchemaBoard): pass

class ResponseBoard(SchemaBoard): pass

class UpdateBoard(SchemaBoard): pass
