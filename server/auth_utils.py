from types import new_class
import jwt
from fastapi import HTTPException
from passlib.context import CryptContext # To hash passwords
from datetime import datetime, timedelta
from decouple import config

JWT_KEY = config('JWT_KEY')

class AuthJwtCsrf():
  # bcrypt is a password-hashing function, based on the Blowfish cipher
  pwd_ctx = CryptContext(schemes=['bcrypt'], deprecated='auto')
  secret_key = JWT_KEY

<<<<<<< HEAD
  def generate_hashed_pw(self, password) -> str:
    return self.pwd_ctx.hash(password)

  def verify_pw(self,plain_pw, hashed_pw) -> bool:
=======
  def generate_hashed_pw(selt, pw):
    return selt.pwd_ctx.hash(pw)
  
  def verify_pw(self,plain_pw, hashed_pw):
>>>>>>> ff0d9b1eb815b8034ef76e605cd9f5367a658217
    return self.pwd_ctx.verify(plain_pw, hashed_pw)

  def encode_jwt(self,email) -> str:
    payload = {
      # datetime.utcnow(): returns the current UTC date and time, as a naive datetime object.
      # timedelta(): returns a timedelta object representing a duration of time.
      'exp': datetime.utcnow() + timedelta(days=0, minutes=5), # JWT Token will expride in 5 minutes
      'iat': datetime.utcnow(), # JWT Token will be created at the time of issuing
      'sub': email
    }
    # Generate JWT Token
    return jwt.encode(
      payload,
      self.secret_key,
      algorithm='HS256' # HS256 requires one secret key
    )

  def decode_jwt(self,token) -> str:
    try:
      payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
      return payload['sub']
    except jwt.ExpiredSignatureError:
      raise HTTPException(status_code=401, detail='Token expired')
    except jwt.InvalidTokenError as e: # Added 'as e' to catch the exception
      raise HTTPException(status_code=401, detail='Invalid token')
    
<<<<<<< HEAD
  def verify_jwt(self,request) -> str:
=======
  def verify_jwt(self,request):
>>>>>>> ff0d9b1eb815b8034ef76e605cd9f5367a658217
    # Get access token from Cookie
    token = request.cookies.get('access_token')
    if not token:
      raise HTTPException(status_code=401, detail='No JWT token')
    # Split the token into 3 parts: header, separator, and payload
    _,_,value = token.partition(' ') # value is the token
    subject = self.decode_jwt(value) # Decode the token. If it is expired, it will raise an exception
    return subject

  def verify_update_jwt(self, request) -> tuple[str,str]:
    subject = self.verify_jwt(request) # Get the email from the JWT token
    new_token = self.encode_jwt(subject) # Generate a new JWT token
    return new_token, subject # Return the new JWT token and the email from the JWT token

  def verify_csrf_update_jwt(self, request, csrf_protect, headers) -> str:
    csrf_token = csrf_protect.get_csrf_from_headers(headers) # Get the CSRF token from the headers
    csrf_protect.validate_csrf(csrf_token) # Validate the CSRF token
    subject = self.verify_jwt(request) # Get the email from the JWT token
    new_token = self.encode_jwt(subject) # Generate a new JWT token
    return new_token # Return the new JWT token
