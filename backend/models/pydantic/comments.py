from pydantic import BaseModel

class SchemaComment(BaseModel):
    text: str

class CreateComment(SchemaComment): pass

class ResponseComment(SchemaComment): pass

class UpdateComment(BaseModel): 
    text: str | None = None