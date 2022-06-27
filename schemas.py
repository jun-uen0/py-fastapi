from pydantic import BaseModel
from typing import Optional

class Todo(BaseModel):
  id: str
  title: str
  description: str

class TodoBody(BaseModel):
  title: str
  description: str

class SuccessMsg(BaseModel):
  message: str

class Userinfo(BaseModel):
  id: Optional[str] = None
  email: str
