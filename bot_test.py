import asyncio
from telethon.sync import TelegramClient, events
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
from form_filler import cappa_register


bot = TelegramClient(
    "bot", settings.api_id, settings.api_hash, sequential_updates=True
).start(bot_token=settings.bot_token)

user_data = {"username": None, "email": None, "password": None}
text_data = ""


@bot.on(events.NewMessage(pattern="/start"))
async def start(event):
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
    await event.respond("enter username, email and password separated by commas")


@bot.on(events.NewMessage(pattern=r"^([^,]+),([^,]+),([^,]+)$"))
async def save_data(event):
    if isinstance(event.peer_id, PeerUser):
        print(event.raw_text)
        text_data = event.raw_text.split(",")
        user_data["username"] = text_data[0]
        user_data["email"] = text_data[1]
        user_data["password"] = text_data[2]
        print(user_data)
        print(event.peer_id)
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
            message=f"your username: {user_data['username']}, email: {user_data['email']}, aaaand password i'll keep in secret",
            buttons=keyboard,
        )
        

async def main():
    await bot.disconnect()


with bot.run_until_disconnected():
    asyncio.run(main())
