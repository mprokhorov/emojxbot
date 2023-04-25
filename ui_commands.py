from aiogram import Bot
from aiogram.types import BotCommandScopeAllPrivateChats, BotCommand


async def set_ui_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="Restart bot"),
        BotCommand(command="new", description="Create new set"),
        BotCommand(command="split", description="Split image to tiles"),
        BotCommand(command="delete", description="Delete set")
    ]
    await bot.set_my_commands(
        commands=commands,
        scope=BotCommandScopeAllPrivateChats()
    )
