from pydantic import BaseModel

class TodoBody(BaseModel):
  title: str
  description: str