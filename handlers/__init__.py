from aiogram import Dispatcher
from aiogram.dispatcher.filters import CommandStart, CommandHelp

from common.commands import CommandMenu, CommandPublishReview, CommandSetReminder, CommandUnSetReminder
from keyboard.callbacks import MenuCallBack, ReviewCallBack
from keyboard.keyboards import MainMenu, TaskMenuOnReview, TaskMenuConfirmed
from .common_handlers import start, help
from .error_handlers import errors_handler
from .menu_handlers import show_main_menu, show_all_user_tasks, show_adm_menu
from .task_handlers import publish_task_for_review, set_global_reminder, unset_global_reminder, take_review_task, \
    confirm_review_task


def setup(dp: Dispatcher):
    # Common
    dp.register_message_handler(start, CommandStart())
    dp.register_message_handler(help, CommandHelp())

    # Errors
    dp.register_errors_handler(errors_handler)

    # Menu
    dp.register_message_handler(show_main_menu, CommandMenu())
    dp.register_callback_query_handler(show_all_user_tasks, MenuCallBack.filter(action=MainMenu.get_tasks))
    dp.register_callback_query_handler(show_adm_menu, MenuCallBack.filter(action=MainMenu.show_adm_menu))

    # Tasks
    dp.register_message_handler(publish_task_for_review, CommandPublishReview())
    dp.register_message_handler(set_global_reminder, CommandSetReminder())
    dp.register_message_handler(unset_global_reminder, CommandUnSetReminder())
    dp.register_callback_query_handler(take_review_task, ReviewCallBack.filter(action=TaskMenuOnReview.take))
    dp.register_callback_query_handler(confirm_review_task, ReviewCallBack.filter(action=TaskMenuConfirmed.confirmed))





