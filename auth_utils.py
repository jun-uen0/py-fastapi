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

  def generate_hashed_pw(selt, pw):
    return selt.pwd_ctx.hash(pw)
  
  def verity_pw(self,plain_pw, hashed_pw):
    return self.pwd_ctx.verify(plain_pw, hashed_pw)
  
  def encode_jwt(self,email):
    payload = {
      # datetime.utcnow(): returns the current UTC date and time, as a naive datetime object.
      # timedelta(): returns a timedelta object representing a duration of time.
      'exp': datetime.utcnow() + timedelta(days=0, minutes=5), # JWT Token will expride in 5 minutes
      'iat': '',
      'sub': email
    }
    # Generate JWT Token
    return jwt.encode(
      payload,
      self.secret_key,
      algorithm='HS256' # HS256 requires one secret key
    )

  def decode_jwt(self,token):
    try:
      payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
      return payload['sub']
    except jwt.ExpiredSignatureError:
      raise HTTPException(status_code=401, detail='Token expired')
    except jwt.InvalidTokenError:
      raise HTTPException(status_code=401, detail='Invalid token')
    
  def verity_jwt(self,request):
    # Get access token from Cookie
    token = request.cookies.get('access_token')
