from ..database.database import create_user, get_hash_db, get_login_db
class UserService():

    @staticmethod
    async def add_user(new_user):
        await create_user(new_user)

    @staticmethod
    async def get_password_hash_us(login):
        return await get_hash_db(login)

    @staticmethod
    async def get_login_us(login):
        return await get_login_db(login)