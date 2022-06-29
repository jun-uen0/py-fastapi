from fastapi import APIRouter
from fastapi import Response, Request, Depends
from fastapi.encoders import jsonable_encoder
from schemas import UserBody, SuccessMsg, UserInfo, Csrf
from db import (
  db_signup,
  db_login,
)
from auth_utils import AuthJwtCsrf
from fastapi_csrf_protect import CsrfProtect

router = APIRouter()
auth = AuthJwtCsrf()

@router.get("/api/csrf-token", response_model=Csrf)
async def get_csrf_token(csrf_protect: CsrfProtect = Depends()):
  csrf_token = csrf_protect.generate_csrf() 
  res = {'csrf_token': csrf_token}
  return res

@router.post("/api/register", response_model=UserInfo)
async def signup(request: Request, user: UserBody, csrf_protect: CsrfProtect = Depends()): 
  csrf_token = csrf_protect.get_csrf_from_headers(request.headers)
  csrf_protect.validate_csrf(csrf_token)
  user = jsonable_encoder(user) # convert to dict
  new_user = await db_signup(user)
  return new_user

@router.post("/api/login", response_model=SuccessMsg)
async def login(request: Request, response: Response, user: UserBody, csrf_protect: CsrfProtect = Depends()):
  csrf_token = csrf_protect.get_csrf_from_headers(request.headers)
  csrf_protect.validate_csrf(csrf_token)
  user = jsonable_encoder(user)
  token = await db_login(user)
  response.set_cookie( # Place token in cookie
    key="access_token", value=f"Bearer {token}", httponly=True, samesite="none", secure=True)
  return {"message": "Successfully login"}
