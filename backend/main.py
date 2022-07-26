from fastapi import FastAPI, Form, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseSettings
from functools import lru_cache
from google.oauth2 import id_token
from google.auth.transport import requests
import requests as req

app = FastAPI()

class Settings(BaseSettings):
    client_secret:str
    ui_url:str

@lru_cache()
def get_settings():
    return Settings()

origins=[get_settings().ui_url]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"msg": "Hello World"}

@app.post("/user/google")
async def auth_google(code: str = Form(), client_id: str = Form()):
    settings = get_settings()
    url='https://accounts.google.com/o/oauth2/token'
    params = {"grant_type":"authorization_code","code":code,"client_id":client_id,"client_secret":settings.client_secret, "redirect_uri":settings.ui_url +"login"}
    r = await req.post(url, params=params).json()
    try:
        idinfo = id_token.verify_oauth2_token(r['id_token'], requests.Request(), client_id)
        userid = idinfo['sub']
        return userid
    except ValueError:
        return None
    
@app.get("/auth/user")
async def get_user():
    return None