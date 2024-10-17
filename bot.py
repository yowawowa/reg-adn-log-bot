import asyncio
from telethon.sync import TelegramClient, events, Button
from telethon.tl.types import (
    PeerChannel,
    PeerUser,
    ReplyKeyboardMarkup,
    ReplyInlineMarkup,
)
from app.config import settings


bot = TelegramClient(
    "bot", settings.api_id, settings.api_hash, sequential_updates=True
).start(bot_token=settings.bot_token)

register_board = [
    [Button.inline("username", b"username"), Button.inline("email", b"mail")],
    [Button.inline("back", b"back")],
]


# says hi
@bot.on(events.NewMessage)
async def my_event_handler(event):
    if "hello" in event.raw_text:
        await event.reply("hi!")


# start conversation
@bot.on(events.NewMessage(pattern="/start"))
async def start(event):
    keyboard = [
        [Button.inline("register", b"register"), Button.inline("login", b"login")],
    ]

    await bot.send_message(
        event.chat_id,
        "Hello! I'm your friendly bot. "
        "You can use me to fill in the forms on the CAPPA website.",
        buttons=keyboard,
    )


user_data = {"username": None, "email": None}


# @bot.on(events.ChatAction)
# async def my_event_handler(event): ...


@bot.on(events.CallbackQuery(data=b"register"))
async def registration_callback(event):
    await bot.send_message(
        event.chat_id,
        "credentials from reg",
        buttons=register_board,
    )


@bot.on(events.CallbackQuery(data=b"username"))
async def username_callback(event):

    await bot.send_message(event.chat_id, "enter username")

    @bot.on(events.NewMessage)
    async def save_username(event):
        user_data["username"] = event.raw_text

        await bot.send_message(
            event.chat_id, "credentials from user", buttons=register_board
        )


@bot.on(events.CallbackQuery(data=b"mail"))
async def email_callback(event):

    await bot.send_message(event.chat_id, "enter email")

    @bot.on(events.NewMessage)
    async def save_email(event):
        user_data["email"] = event.raw_text

        await bot.send_message(
            event.chat_id, "credentials from email", buttons=register_board
        )


# @bot.on(events.CallbackQuery)
# async def email_callback(event):
#     if event.data == b"mail":
#         await bot.send_message(event.chat_id, "enter email")


# @bot.on(events.CallbackQuery)
# async def email_callback(event):
#     if event.data == b"email":
#         await event.respond("enter email")

#         @bot.on(events.NewMessage)
#         async def save_email(event):
#             user_data["email"] = event.raw_text
#             await event.respond("credentials from email", buttons=main_board)


@bot.on(events.CallbackQuery)
async def back_callback(event):
    if event.data == b"back":
        # await start(event)
        ...


async def main():
    await bot.disconnect()


with bot.run_until_disconnected():
    asyncio.run(main())
