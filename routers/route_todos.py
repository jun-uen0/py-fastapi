from fastapi import APIRouter
from fastapi import Request, Response, HTTPException
from fastapi.encoders import jsonable_encoder
from schemas import Todo, TodoBody, SuccessMsg
from db import db_create_todo, db_get_todos, db_get_single_todo, db_update_single_todo, db_delete_single_todo
from typing import List
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

@router.get("/api/todos", response_model=List[Todo])
async def get_todos(request: Request):
  # Here Jwt Token handling logic can be added
  res = await db_get_todos()
  if res:
    return res
  raise HTTPException(
    status_code=404, detail="Get todos failed")

@router.get("/api/todo/{id}", response_model=Todo)
async def get_single_todo(request: Request, response: Response, id: str):
  # Here CSRF Token handling logic can be added
  # Set cookie
  res = await db_get_single_todo(id)
  if res:
    return res
  raise HTTPException(
    status_code=404, detail=f"Get todo of id:{id} failed")

@router.put("/api/todo/{id}", response_model=Todo)
async def update_single_todo(request: Request, response: Response, id: str, data: TodoBody):
  # Here CSRF Token handling logic can be added
  # Set cookie
  todo = jsonable_encoder(data)
  res = await db_update_single_todo(id,todo)
  if res:
    return res
  raise HTTPException(
    status_code=404, detail=f"Update todo of id:{id} failed")

@router.delete("/api/todo/{id}", response_model=SuccessMsg)
async def delete_single_todo(request: Request, response: Response, id: str):
  # Here CSRF Token handling logic can be added
  # Set cookie
  res = await db_delete_single_todo(id)
  if res:
    return {'message': 'Successfully deleted'}
  raise HTTPException(
    status_code=404, detail=f"Delete todo of id:{id} failed")