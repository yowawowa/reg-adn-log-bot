bot = TelegramClient(
    "bot", settings.api_id, settings.api_hash, sequential_updates=True
).start(bot_token=settings.bot_token)

user_input = {"username": None, "password": None, "email": None}


@bot.on(events.CallbackQuery)
async def registration_callback(event):
    if event.data == b"register":
        keyboard = [
            [
                Button.inline("username", b"username"),
                Button.inline("email", b"email"),
                Button.inline("back", b"mainmenu"),
            ]
        ]
        await bot.send_message(
            event.chat_id,
            "enter kredentials",
            buttons=keyboard,
        )


@bot.on(events.CallbackQuery)
async def main_menu(event):
    if event.data == b"mainmenu":
        await event.respond("You clicked mainmenu")


@bot.on(events.CallbackQuery)
async def username_callback(event):
    if event.data == b"username":
        await event.respond("enter username")

        @bot.on(events.NewMessage)
        async def username_save(event):
            if event:
                user_input["username"] = event.raw_text
            await event.respond(f"saved {user_input["username"]} as username")
            keyboard = [
                [
                    Button.inline("email", b"email"),
                    Button.inline("password", b"password"),
                ]
            ]

            await bot.send_message(
                event.chat_id,
                "enter kredentials",
                buttons=keyboard,
            )


@bot.on(events.CallbackQuery)
async def email_callback(event):
    if event.data == b"email":
        await event.respond("enter email")

        @bot.on(events.NewMessage)
        async def email_save(event):
            if event:
                user_input["email"] = event.raw_text
            await event.respond(f"saved {user_input["email"]} as email")

            keyboard = [
                [
                    Button.inline("password", b"password"),
                ]
            ]

            await bot.send_message(
                event.chat_id,
                "enter kredentials",
                buttons=keyboard,
            )


@bot.on(events.CallbackQuery)
async def password_callback(event):
    if event.data == b"password":
        await event.respond("enter password")

        @bot.on(events.NewMessage)
        async def password_save(event):
            if event:
                user_input["password"] = event.raw_text
            await event.respond(f"saved {user_input['password']} as password")

            keyboard = [
                [
                    Button.inline("send", b"send"),
                ]
            ]

            await bot.send_message(
                event.chat_id,
                "time to send",
                buttons=keyboard,
            )


@bot.on(events.CallbackQuery)
async def send_callback(event):
    if event.data == b"send":
        await event.respond("sending")
        await register(**user_input)
