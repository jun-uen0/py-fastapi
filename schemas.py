from pydantic import BaseModel
from typing import Optional
from decouple import config

CSRF_KEY = config['CSRF_KEY']

class CsrfSettings(BaseModel):
  secret_key: str = CSRF_KEY

class Csrf(BaseModel):
  csrf_token: str

class Todo(BaseModel):
  id: str
  title: str
  description: str

class TodoBody(BaseModel):
  title: str
  description: str

class SuccessMsg(BaseModel):
  message: str

  id: Optional[str] = None
  email: str

class UserBody(BaseModel):
  email: str
  password: str