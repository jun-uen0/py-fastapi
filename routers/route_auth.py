from fastapi import APIRouter
from fastapi import Response
from fastapi.encoders import jsonable_encoder
from schemas import UserBody, SuccessMsg, UserInfo
from db import (
  db_signup,
  db_login,
)
from auth_utils import AuthJwtCsrf

router = APIRouter()
auth = AuthJwtCsrf()

@router.post("/api/register", response_model=UserInfo)
async def signup(user: UserBody):
  user = jsonable_encoder(user) # convert to dict
  new_user = await db_signup(user)
  return new_user

@router.post("/api/login", response_model=SuccessMsg)
async def login(response: Response, user: UserBody):
  user = jsonable_encoder(user)
  token = await db_login(user)
  response.set_cookie( # Place token in cookie
    key="access_token", value=f"Bearer {token}", httponly=True, samesite="none", secure=True)
  return {"message": "Successfully login"}