from aiogram import Dispatcher
from aiogram import types
from aiogram.dispatcher.filters import Command, CommandStart, CommandHelp


class CommandMenu(Command):
    def __init__(self):
        super().__init__(['menu'])


class CommandPublishReview(Command):
    def __init__(self):
        super().__init__(['review'])


class CommandSetReminder(Command):
    def __init__(self):
        super().__init__(['set_reminder'])


class CommandUnSetReminder(Command):
    def __init__(self):
        super().__init__(['unset_reminder'])


async def set_default_commands(dp: Dispatcher) -> None:
    await dp.bot.set_my_commands(
        [
            types.BotCommand(CommandHelp().commands[0], "Show help"),
            types.BotCommand(CommandStart().commands[0], "Start bot"),

            types.BotCommand(CommandMenu().commands[0], "Show main menu"),

            types.BotCommand(CommandPublishReview().commands[0], "Submit link to review"),
        ]
    )