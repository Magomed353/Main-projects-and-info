import asyncio
import bcrypt
from fastapi import FastAPI, status, HTTPException, Depends
from fastapi.responses import JSONResponse
from .jwt_service import *
from .user_service import UserService 
from .model import UserSchema, TokenSchema


class auth_service():

    @staticmethod
    async def registration(login, password):
        if await UserService.get_login_us(login) != None:
            raise JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"status": False, "message":"Логин уже существует"}
            )
        password_hash = auth_service.hash_password(password)
        new_user = UserSchema(login=login, password_hash=password_hash)
        await UserService.add_user(new_user)
        return  JSONResponse(
                    status_code=status.HTTP_201_CREATED,
                    content={"status": True, "message":"Регистрация прошла успешно"}
                )
    
    @staticmethod 
    async def authentification(user):
        error = HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={"status": False, "message": "Неверный логин или пароль"}
                )
        if await auth_service.verify_auth_data(user.login, user.password_hash) == False:
            raise error
        return user

    @staticmethod
    async def authorization():
        pass

    @staticmethod
    async def hash_password(password):
        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")
        return password_hash
    
    @staticmethod
    async def verify_auth_data(login, password):
        hash = await UserService.get_password_hash_us(login)
        if hash == None:
            return False
        if not bcrypt.checkpw(password.encode("utf-8"), hash.encode("utf-8")):
            return False
        return True

исправил проверку пароля, осталось закончить  авторизацию через jwt и можно
идти дальше  