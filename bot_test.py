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


bot = TelegramClient(
    "bot", settings.api_id, settings.api_hash, sequential_updates=True
).start(bot_token=settings.bot_token)


@bot.on(events.NewMessage(pattern="/start"))
async def start(event):
    if isinstance(event.peer_id, PeerUser):
        keyboard_buttons = ReplyKeyboardMarkup(
            [
                KeyboardButtonRow(
                    [
                        KeyboardButton(
                            text="Menu",
                        )
                    ],
                )
            ]
        )
        await bot.send_message(
            entity=event.peer_id, message="иу", buttons=keyboard_buttons
        )


@bot.on(events.NewMessage(pattern="Menu"))
async def menu(event):
    if isinstance(event.peer_id, PeerUser):
        keyboard_buttons = ReplyInlineMarkup(
            [
                KeyboardButtonRow(
                    [
                        KeyboardButtonUrl(text="eto link", url="sex.com"),
                        KeyboardButtonCallback(text="eto colbek", data=b"user"),
                    ]
                )
            ]
        )

        await bot.send_message(
            entity=event.peer_id, message="inlain", buttons=keyboard_buttons
        )


@bot.on(events.CallbackQuery(data=b"user"))
async def get_user(event):
    await event.respond("uspeh")


async def main():
    await bot.disconnect()


with bot.run_until_disconnected():
    asyncio.run(main())
