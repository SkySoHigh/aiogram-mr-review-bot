from aiogram import Dispatcher
from aiogram.dispatcher.filters import CommandStart, CommandHelp

from common.commands import CommandMenu, CommandPublishReview, CommandSetReminder, CommandUnSetReminder
from keyboard.callbacks import MenuCallBack, ReviewCallBack
from keyboard.keyboards import MainMenu, TaskMenuOnReview, TaskMenuReviewFinished, TaskMenuFinalReview
from .common_handlers import start, help
from .error_handlers import errors_handler
from .menu_handlers import show_main_menu, show_adm_menu
from .notifier_handler import set_global_reminder, unset_global_reminder
from .task_handlers import publish_task_for_review, take_task_on_review_cb, \
    confirm_reviewed_task_cb, send_user_tasks_on_review_to_pm, reject_reviewed_task, submit_reviewed_task_cb, \
    send_all_tasks_on_review_to_chat


def setup(dp: Dispatcher):
    # Common
    dp.register_message_handler(start, CommandStart())
    dp.register_message_handler(help, CommandHelp())

    # Errors
    dp.register_errors_handler(errors_handler)

    # Menu
    dp.register_message_handler(show_main_menu, CommandMenu())
    dp.register_callback_query_handler(send_user_tasks_on_review_to_pm,
                                       MenuCallBack.filter(action=MainMenu.send_tasks_to_pm))
    dp.register_callback_query_handler(send_all_tasks_on_review_to_chat,
                                       MenuCallBack.filter(action=MainMenu.send_tasks_to_group_chat), is_admin=True)
    dp.register_callback_query_handler(show_adm_menu, MenuCallBack.filter(action=MainMenu.show_adm_menu), is_admin=True)

    # Tasks
    dp.register_message_handler(publish_task_for_review, CommandPublishReview())
    dp.register_message_handler(set_global_reminder, CommandSetReminder())
    dp.register_message_handler(unset_global_reminder, CommandUnSetReminder())

    dp.register_callback_query_handler(take_task_on_review_cb, ReviewCallBack.filter(action=TaskMenuOnReview.take))
    dp.register_callback_query_handler(submit_reviewed_task_cb,
                                       ReviewCallBack.filter(action=TaskMenuFinalReview.submitted))
    dp.register_callback_query_handler(confirm_reviewed_task_cb,
                                       ReviewCallBack.filter(action=TaskMenuReviewFinished.confirmed))
    dp.register_callback_query_handler(reject_reviewed_task,
                                       ReviewCallBack.filter(action=TaskMenuReviewFinished.canceled))
