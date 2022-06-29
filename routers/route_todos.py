from fastapi import APIRouter
from fastapi import Request, Response, HTTPException, Depends # Depends is a dependency injection function
from fastapi.encoders import jsonable_encoder
from schemas import Todo, TodoBody, SuccessMsg
from db import db_create_todo, db_get_todos, db_get_single_todo, db_update_single_todo, db_delete_single_todo
from typing import List
from fastapi_csrf_protect import CsrfProtect
from auth_utils import AuthJwtCsrf

router = APIRouter()
auth = AuthJwtCsrf()

@router.post("/api/todo", response_model=Todo)
async def create_todo(request: Request, response: Response, data: TodoBody, csrf_protect: CsrfProtect = Depends()):
  # Verify the CSRF token
  new_token = auth.verify_csrf_update_jwt(request, csrf_protect, request.headers)
  todo = jsonable_encoder(data)
  res = await db_create_todo(todo)
  response.status_code = 201
  response.set_cookie(
    key='access_token',
    value=f'Bearer {new_token}',
    httponly=True, # This cookie is only accessible by the browser
    samesite='none', # Becouse the app is Single page application, this cookie is not accessible by other sites
    secure=True # This cookie is only accessible by https
  )
  if res:
    return res
  else:
    return HTTPException(status_code=404, detail="Todo creation failed")

@router.get("/api/todos", response_model=List[Todo])
async def get_todos(request: Request):
  auth.verity_jwt(request)
  res = await db_get_todos()
  if res:
    return res
  raise HTTPException(
    status_code=404, detail="Get todos failed")

@router.get("/api/todo/{id}", response_model=Todo)
async def get_single_todo(request: Request, response: Response, id: str):
  new_token,_ = auth.verify_csrf_update_jwt(request) # _ is a payload. We don't need it here
  res = await db_get_single_todo(id)
  response.set_cookie(
    key='access_token',
    value=f'Bearer {new_token}',
    httponly=True, # This cookie is only accessible by the browser
    samesite='none', # Becouse the app is Single page application, this cookie is not accessible by other sites
    secure=True # This cookie is only accessible by https
  )
  if res:
    return res
  raise HTTPException(
    status_code=404, detail=f"Get todo of id:{id} failed")

@router.put("/api/todo/{id}", response_model=Todo)
async def update_single_todo(request: Request, response: Response, id: str, data: TodoBody, csrf_protect: CsrfProtect = Depends()):
  new_token = auth.verify_csrf_update_jwt(request, csrf_protect, request.headers)
  todo = jsonable_encoder(data)
  res = await db_update_single_todo(id,todo)
  response.set_cookie(
    key='access_token',
    value=f'Bearer {new_token}',
    httponly=True, # This cookie is only accessible by the browser
    samesite='none', # Becouse the app is Single page application, this cookie is not accessible by other sites
    secure=True # This cookie is only accessible by https
  )
  if res:
    return res
  raise HTTPException(
    status_code=404, detail=f"Update todo of id:{id} failed")

@router.delete("/api/todo/{id}", response_model=SuccessMsg)
async def delete_single_todo(request: Request, response: Response, id: str):
  new_token = auth.verify_csrf_update_jwt(request)
  res = await db_delete_single_todo(id)
  response.set_cookie(
    key='access_token',
    value=f'Bearer {new_token}',
    httponly=True, # This cookie is only accessible by the browser
    samesite='none', # Becouse the app is Single page application, this cookie is not accessible by other sites
    secure=True # This cookie is only accessible by https
  )
  if res:
    return res
  raise HTTPException(
    status_code=404, detail=f"Delete todo of id:{id} failed")