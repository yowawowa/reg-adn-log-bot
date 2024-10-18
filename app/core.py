from encoding_manager import encode_password, decode_password
from sqlalchemy.ext.asyncio import async_sessionmaker
from app.database import async_engine
from app.models import User
from sqlalchemy.future import select
from pydantic import BaseModel
from form_filler import cappa_login

AsyncSession = async_sessionmaker(bind=async_engine)


class UserData(BaseModel):
    username: str


async def save_user_to_db(user_data):
    """
    Add new username to database.

    Args:
        username_data (UserData): UserData object.

    Returns:
        {'message': 'Username added'}: Username has been added to the database.
    """
    async with AsyncSession() as session:
        existing_user = await get_user_by_tg_id_and_login(user_data["tg_id"])
        user = User(
            tg_id=user_data["tg_id"],
            username=user_data["username"],
            email=user_data["email"],
            password=encode_password(user_data["password"]),
        )
        if not existing_user:
            session.add(user)
            await session.commit()
            return {"message": "Username added"}
        else:
            return {"message": "Username already exists"}


async def get_user_by_tg_id_and_login(tg_id: str):
    """
    Retrieve a user from the database by tg_id.

    Args:
        tg_id (str): The tg_id to search for.

    Returns:
        User or None: The User object if found, otherwise None.
    """
    async with AsyncSession() as session:
        result = await session.execute(select(User).filter_by(tg_id=tg_id))
        user_data = result.scalar()
        if user_data:
            await cappa_login(
                user_data.username, decode_password(user_data.password)
            )  # how to unhash?
            return {
                "username": user_data.username,
                "password": user_data.password,
            }
        return user_data
