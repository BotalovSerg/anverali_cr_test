from aiogram import Bot
from aiogram.types import BotCommand


async def set_main_menu(bot: Bot) -> None:
    main_menu_commands = [
        BotCommand(
            command="/add",
            description="Добовление задачи",
        ),
        BotCommand(
            command="/tsk",
            description="Список всех задач",
        ),
    ]
    await bot.set_my_commands(main_menu_commands)
