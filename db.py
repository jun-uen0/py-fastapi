import email
from http import client
from click import password_option
from fastapi import HTTPException
from typing import Collection
from decouple import config
from typing import Union
from bson import ObjectId
import motor.motor_asyncio
from auth_utils import AuthJwtCsrf

MONGO_API_KEY=config('MONGO_API_KEY')
client=motor.motor_asyncio.AsyncIOMotorClient(MONGO_API_KEY)

db = client.FastAPI01
cll_todos = db.todos
cll_users = db.users
auth = AuthJwtCsrf()

def todo_serializer(todo: dict) -> dict:
  return {
    "id": str(todo["_id"]),
    "title": todo["title"],
    "description": todo["description"]
  }

def user_serializer(user) -> dict:
  return {
    "id": str(user["_id"]),
    "email": user["email"],
  }

async def db_create_todo(todo: dict) -> Union[dict, bool]:
  todo = await cll_todos.insert_one(todo)
  new_todo = await cll_todos.find_one({'_id': todo.inserted_id})
  if new_todo:
    return todo_serializer(new_todo)
  return False

async def db_get_todos() -> list:
  todos = []
  for todo in await cll_todos.find().to_list(length=100): # to_list() gets all the documents in the collection
    todos.append(todo_serializer(todo))
  return todos

async def db_get_single_todo(id: str) -> Union[dict, bool]:
  todo = await cll_todos.find_one({'_id': ObjectId(id)})
  if todo:
    return todo_serializer(todo)
  return False

async def db_update_single_todo(id: str, data: dict) -> Union[dict, bool]:
  todo = await cll_todos.find_one({'_id': ObjectId(id)})
  if todo: 
    # continue if todo is not None
    updated_todo = await cll_todos.update_one( 
      # update_one() return UpdateResult class
      {'_id': ObjectId(id)}, {"$set": data}
    )
    if updated_todo.modified_count > 0: 
      # UpdateResult class has modified_count attribute
      # If the modified_count is larger than zero, the update was successful
      new_todo = await cll_todos.find_one({"_id": ObjectId(id)})
      return todo_serializer(new_todo)
  return False

async def db_delete_single_todo(id: str) -> bool:
  todo = await cll_todos.delete_one({'_id': ObjectId(id)})
  if todo:
    deleted_todo = await cll_todos.delete_one( 
      # update_one() return UpdateResult class
      {'_id': ObjectId(id)}
    )
    if deleted_todo.deleted_count > 0:
      # UpdateResult class has deleted_count attribute
      # If the deleted_count is larger than zero, the delete was successful
      return True
  return False

async def db_signup(data: dict) -> dict: # return user data
  email = data.get('email')
  password = data.get('password')

  # Check if email is already in use
  overlap_user = await cll_users.find_one({'email': email})
  if overlap_user:
    raise HTTPException(status_code=400, detail={'message': 'Email already in use'})
  # Check if password is zero or less than 6 characters
  if not password or len(password) < 6:
    raise HTTPException(status_code=400, detail={'message': 'Password is too short'})
  # Insert user with email and hashed password
  user = await cll_users.insert_one({"email": email, "password": auth.generate_hashed_pw(password)})
  new_user = await cll_users.find_one({"_id": user.inserted_id})
  return user_serializer(new_user)

async def db_login(data: dict) -> dict: # return JWT token
  email = data.get('email')
  password = data.get('password')
  user = await cll_users.find_one({'email': email})
  if not user:
    raise HTTPException(status_code=400, detail={'message': 'Email not found'})
  if not auth.verity_jwt(password, user['password']):
    raise HTTPException(status_code=400, detail={'message': 'Wrong password'})
  token = auth.encode_jwt(user['email'])
  return token