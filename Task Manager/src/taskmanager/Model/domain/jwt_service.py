import jwt
import bcrypt 
from datetime import timedelta, datetime
from ...config import AuthJWT
from fastapi import Depends
from .model  import UserSchema
from .aut_service import auth_service
auth_jwt = AuthJWT()

class JwtTools:
    async def encode_jwt(
            payload: dict, 
            private_key=auth_jwt.private_key_path.read_text(), 
            algorithm=auth_jwt.algorithm,
            expire_minutes: int = auth_jwt.access_token_expire_minutes,
            expire_timedelta: timedelta| None = None,
            
        ):
        to_encode = payload.copy()
        now = datetime.utcnow()
        if expire_timedelta:
            expire = now + timedelta
        else:
            expire = now + timedelta(minutes=expire_minutes)
        to_encode.update(
            exp=expire,
            iat=now,
            )
        encoded = await jwt.encode(to_encode, private_key, algorithm=algorithm)

        return encoded

    async def decode_jwt( 
            token : str | bytes , 
            public_key : str = auth_jwt.public_key_path.read_text(), 
            algorithm: str = auth_jwt.algorithm
        ):
        decoded = encoded = jwt.decode(token, public_key, algorithm=algorithm)
        return decoded

    async def authorization(user :UserSchema):
        auth_service.ait
        jwt_payload = {"username": user.login}
        token = JwtTools.encode_jwt(jwt_payload)
        return 