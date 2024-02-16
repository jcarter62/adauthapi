from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from adauth import ADAuth
from decouple import config

app = FastAPI()

allowed_hosts = config("ALLOWED_HOSTS").split(",")

print(allowed_hosts)


@app.middleware("http")
async def check_hosts(request: Request, call_next):
    global allowed_hosts
    client_host = request.client.host
    if client_host in allowed_hosts:
        response = await call_next(request)
        return response
    else:
        data = {"message": "Host not allowed"}
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content=data)

class AuthDetails(BaseModel):
    username: str
    password: str


@app.post("/auth")
async def auth(auth_details: AuthDetails):
    return auth_group(auth_details, group='')


@app.post("/auth/{group}")
async def auth_group(auth_details: AuthDetails, group: str):
    if group <= '':
        adauth = ADAuth()
    else:
        adauth = ADAuth(groupname=group)

    if config('DEBUG','False') == 'True':
        print(f"Authenticating user: {auth_details.username}, ({auth_details.password}) with group: {group}")

    authenticated = adauth.authenticate_user(auth_details.username, auth_details.password)

    if authenticated == 0:
        data = {"message": "fail"}
        result = status_code = status.HTTP_401_UNAUTHORIZED

    if authenticated == 1:
        data = {"message": "user authenticated, group not found"}
        result = status_code = status.HTTP_206_PARTIAL_CONTENT

    if authenticated == 2:
        data = {"message": "success"}
        result = status.HTTP_200_OK

    return JSONResponse(status_code=result, content=data)


@app.get("/")
async def auth_get():
    # Implement your authentication logic here
    # For example, check if the username and password are correct
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": ""})
