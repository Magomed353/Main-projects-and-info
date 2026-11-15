from  fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from  ..Model.domain.aut_service import auth_service
from pydantic import BaseModel
from ..Model.domain.model import UserSchema

from ..Model.database.database import drop_tables as dt, create_tables as ct
app = FastAPI()

@app.post("/registration")
async def registration(user: UserSchema):
    return await auth_service.registration(user.login, user.password_hash)

@app.post("/authentification")
async def authentification(data: UserSchema):
    return await auth_service.authentification(data)

# @app.get()
# async def get_token():
#     pass

@app.delete("/delete")
async def delete_tables():
    return  await dt()

@app.post("/create")
async def create_tables():
    return  await ct()


# Функции выдачи jwt_tokena надо переделать, вынести их отдельно в файл jwt_service

