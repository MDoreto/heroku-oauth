from fastapi import FastAPI, Form, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseSettings
from functools import lru_cache
from google.oauth2 import id_token
from google.auth.transport import requests
from fastapi.security import HTTPBasicCredentials, HTTPBearer
from jose import jwt
import requests as req

class Settings(BaseSettings):
    client_id:str
    client_secret:str
    ui_url:str

@lru_cache()
def get_settings():
    return Settings()
app = FastAPI()
security = HTTPBearer()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/")
async def root():
    return {"msg": "Hello World"}

@app.post("/user/google")
def auth_google(code: str = Form(), client_id: str = Form()):
    settings = get_settings()
    url='https://accounts.google.com/o/oauth2/token'
    params = {"grant_type":"authorization_code","code":code,"client_id":client_id,"client_secret":settings.client_secret, "redirect_uri":settings.ui_url +"/login"}
    r = req.post(url, params=params).json()
    try:
        idinfo = id_token.verify_oauth2_token(r['id_token'], requests.Request(), client_id)
        userid = idinfo['sub']
        return userid
    except ValueError:
        print("Error")
        return None
    
@app.get("/auth/user")
async def get_user(credentials: HTTPBasicCredentials = Depends(security)):
    token = credentials.credentials
    return token