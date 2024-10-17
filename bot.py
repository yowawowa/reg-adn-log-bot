import asyncio
from telethon.sync import TelegramClient, events, Button
from app.config import settings


bot = TelegramClient(
    "bot", settings.api_id, settings.api_hash, sequential_updates=True
).start(bot_token=settings.bot_token)

main_board = [
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


@bot.on(events.CallbackQuery)
async def registration_callback(event):
    if event.data == b"register":
        keyboard = [
            [
                Button.inline("username", b"username"),
                Button.inline("email", b"mail"),
            ],
            [Button.inline("back", b"back")],
        ]
        print("from iside")
        await bot.send_message(
            event.chat_id,
            "credentials",
            buttons=keyboard,
        )


@bot.on(events.CallbackQuery)
async def username_callback(event):
    print(event.data)
    if event.data == b"username":
        await event.respond("enter username")

        @bot.on(events.NewMessage)
        async def save_username(event):
            user_data["username"] = event.raw_text

            await event.respond("credentials from user", buttons=main_board)

    await event.answer()


@bot.on(events.CallbackQuery)
async def email_callback(event):
    if event.data == b"mail":
        await event.respond("enter email")

        @bot.on(events.NewMessage)
        async def save_email(event):
            user_data["email"] = event.raw_text

            await event.respond("credentials from email", buttons=main_board)

    await event.answer()


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
