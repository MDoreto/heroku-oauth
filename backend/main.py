from fastapi import FastAPI, Form,Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseSettings
from functools import lru_cache
from google.oauth2 import id_token
from google.auth.transport import requests
from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel
import requests as req

app = FastAPI(title="Heroku Oauth")

origins=["https://prometeon-frontend.herokuapp.com/","https://prometeon-frontend.herokuapp.com","*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AppSettings(BaseSettings):
    client_secret:str
    ui_url:str
    secret_key:str
    class Config:
        env_file='.env'

@lru_cache()
def get_settings():
    return AppSettings()
class Settings(BaseModel):
    authjwt_csrf_methods: set={'GET','POST','PUT','PATCH','DELETE'}
    authjwt_secret_key: str = get_settings().secret_key
    # Configure application to store and get JWT from cookies
    authjwt_token_location: set = {"cookies"}
    # Only allow JWT cookies to be sent over https
    authjwt_cookie_secure: bool = True
    # Enable csrf double submit protection. default is True
    authjwt_cookie_csrf_protect: bool = True
    # Change to 'lax' in production to make your website more secure from CSRF Attacks, default is None
    authjwt_cookie_samesite: str = 'strict'
    authjwt_access_token_expires=43200


@AuthJWT.load_config
def get_config():
    return Settings()
    
@app.get("/")
async def root():
    return {"msg": "Hello World"}

@app.post("/user/google")
def auth_google(code: str = Form(), client_id: str = Form(), Authorize: AuthJWT = Depends()):
    settings = get_settings()
    url='https://accounts.google.com/o/oauth2/token'
    params = {"grant_type":"authorization_code","code":code,"client_id":client_id,"client_secret":settings.client_secret, "redirect_uri":settings.ui_url +"/login"}
    r = req.post(url, params=params).json()
    print(r)
    try:
        idinfo = id_token.verify_oauth2_token(r['id_token'], requests.Request(), client_id)
        userid = idinfo['sub']
        access_token = Authorize.create_access_token(subject=userid)
        Authorize.set_access_cookies(access_token)
        return userid
    except ValueError:
        print("Error")
        return None
    
@app.get("/auth/user")
async def get_user(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    return {"user": current_user}