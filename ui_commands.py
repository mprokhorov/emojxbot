from aiogram import Bot
from aiogram.types import BotCommandScopeAllPrivateChats, BotCommand


async def set_ui_commands(bot: Bot):
    commands = [
        BotCommand(command="new", description="Create new set"),
        BotCommand(command="split", description="Split image to tiles"),
        BotCommand(command="add", description="Make an emoji"),
        BotCommand(command="delete", description="Delete set"),
        BotCommand(command="forwarded", description="Make a GIF")
    ]
    await bot.set_my_commands(
        commands=commands,
        scope=BotCommandScopeAllPrivateChats()
    )
