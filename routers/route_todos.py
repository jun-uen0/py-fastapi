from fastapi import APIRouter
from fastapi import Request, Response, HTTPException
from fastapi.encoders import jsonable_encoder
from schemas import Todo, TodoBody
from db import db_create_todo
# from starlette import HTTP_201_CREATED

router = APIRouter()

@router.post("/api/todo", response_model=Todo)
async def create_todo(request: Request, response: Response, data: TodoBody):
  todo = jsonable_encoder(data)
  res = await db_create_todo(todo)
  response.status_code = 201
  if res:
    return res
  else:
    return HTTPException(status_code=404, detail="Todo creation failed")