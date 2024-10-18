import asyncio
from telethon.sync import TelegramClient, events
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import (
    PeerChannel,
    PeerUser,
    ReplyKeyboardMarkup,
    ReplyInlineMarkup,
    KeyboardButtonRow,
    KeyboardButton,
    KeyboardButtonUrl,
    KeyboardButtonCallback,
)
from app.config import settings
from app.models import create_tables
from form_filler import cappa_register
from app.core import get_user_by_tg_id_and_login, save_user_to_db


bot = TelegramClient(
    "bot", settings.api_id, settings.api_hash, sequential_updates=True
).start(bot_token=settings.bot_token)

user_data = {
    "username": None,
    "email": None,
    "password": None,
    "tg_id": None,
    "first_name": None,
    "last_name": None,
}


@bot.on(events.NewMessage(pattern="/start"))
async def start(event):
    await create_tables()
    if isinstance(event.peer_id, PeerUser):
        keyboard_buttons = ReplyInlineMarkup(
            [
                KeyboardButtonRow(
                    [
                        KeyboardButtonCallback(text="Registration", data=b"reg"),
                        KeyboardButtonCallback(text="Login", data=b"login"),
                    ],
                )
            ]
        )
        await bot.send_message(
            entity=event.peer_id, message="choose one", buttons=keyboard_buttons
        )


@bot.on(events.CallbackQuery(data=b"reg"))
async def registration(event):
    await event.respond(
        "enter username, firs name, lastname, email and password separated by commas"
    )


@bot.on(events.CallbackQuery(data=b"login"))
async def user_login(event):
    user_id = event.query.to_dict()["user_id"]
    print(user_id)
    await get_user_by_tg_id_and_login(user_id)


@bot.on(events.NewMessage(pattern=r"^([^,]+),([^,]+),([^,]+),([^,]+),([^,]+)$"))
async def save_data(event):
    if isinstance(event.peer_id, PeerUser):
        text_data = event.raw_text.split(",")
        user_data["username"] = text_data[0]
        user_data["first_name"] = text_data[1]
        user_data["last_name"] = text_data[2]
        user_data["email"] = text_data[3]
        user_data["password"] = text_data[4]

        user_data["tg_id"] = event.peer_id.to_dict()["user_id"]

        keyboard = ReplyInlineMarkup(
            [
                KeyboardButtonRow(
                    [
                        KeyboardButtonCallback(text="Submit", data=b"submit"),
                        KeyboardButtonCallback(text="Retry", data=b"Retry"),
                    ],
                )
            ]
        )
        await bot.send_message(
            entity=event.peer_id,
            message=f"your username: {user_data['username']}, real name: {user_data['first_name']} {user_data['last_name']}, email: {user_data['email']}, aaaand password i'll keep in secret. press sumbit if u satisfied",
            buttons=keyboard,
        )


@bot.on(events.CallbackQuery(data=b"submit"))
async def save_to_db_and_register(event):
    await save_user_to_db(user_data)
    await cappa_register(user_data)
    await bot.send_message("all done")


async def main():
    await create_tables()
    await bot.disconnect()


with bot.run_until_disconnected():
    asyncio.run(main())
