from enum import Enum

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pydantic import BaseModel

from common import callbacks
from db.models.tasks import TaskStates
from loader import Locale


class TextToCallback(BaseModel):
    text: str
    cb: str


class GroupMainMenu(Enum):
    send_tasks_to_pm = TextToCallback(
        text=Locale.Menu.SHOW_USER_TASKS_BTN, cb="send_task_t_pm"
    )
    send_tasks_to_group_chat = TextToCallback(
        text=Locale.Menu.SHOW_ALL_TASKS_BTN, cb="send_active_tasks_to_chat"
    )
    show_adm_menu = TextToCallback(
        text=Locale.Menu.SHOW_ADM_MENU_BTN, cb="send_active_tasks_to_pm"
    )


class PmMainMenu(Enum):
    get_all_user_tasks = TextToCallback(
        text=Locale.Menu.SHOW_ALL_MY_TASKS, cb="get_all_user_tasks"
    )


class TaskMenuOnReview(Enum):
    take = TextToCallback(text=Locale.Task.TAKE_BTN, cb="take_task")


class TaskMenuReview(Enum):
    submitted = TextToCallback(text=Locale.Task.SUBMIT_BTN, cb="submit_task")
    rejected = TextToCallback(text=Locale.Task.REJECT_BTN, cb="rejected")


class TaskMenuFinalReview(Enum):
    confirmed = TextToCallback(
        text=Locale.Task.FINAL_CONFIRM_BTN, cb="final_confirm_task"
    )
    rejected = TextToCallback(text=Locale.Task.FINAL_REJECT_BTN, cb="final_reject_task")


class TaskMenuFix(Enum):
    fixed = TextToCallback(text=Locale.Task.RESUBMIT_BTN, cb="re_submit_task")


def get_new_task_menu():
    kb = InlineKeyboardMarkup()
    for m in TaskMenuOnReview:
        kb.add(
            InlineKeyboardButton(
                text=m.value.text,
                callback_data=callbacks.ReviewCallBack.new(m.value.cb),
            )
        )
    return kb


def get_review_task_menu():
    kb = InlineKeyboardMarkup()
    for m in TaskMenuReview:
        kb.add(
            InlineKeyboardButton(
                text=m.value.text,
                callback_data=callbacks.ReviewCallBack.new(m.value.cb),
            )
        )
    return kb


def get_final_tasks_menu():
    kb = InlineKeyboardMarkup()
    for m in TaskMenuFinalReview:
        kb.add(
            InlineKeyboardButton(
                text=m.value.text,
                callback_data=callbacks.ReviewCallBack.new(m.value.cb),
            )
        )
    return kb


def get_main_menu_for_group():
    kb = InlineKeyboardMarkup()
    for m in GroupMainMenu:
        kb.add(
            InlineKeyboardButton(
                text=m.value.text, callback_data=callbacks.MenuCallBack.new(m.value.cb)
            )
        )
    return kb


def get_main_menu_for_pm():
    kb = InlineKeyboardMarkup()
    for m in PmMainMenu:
        kb.add(
            InlineKeyboardButton(
                text=m.value.text, callback_data=callbacks.MenuCallBack.new(m.value.cb)
            )
        )
    return kb


def get_task_resubmit_menu():
    kb = InlineKeyboardMarkup()
    for m in TaskMenuFix:
        kb.add(
            InlineKeyboardButton(
                text=m.value.text,
                callback_data=callbacks.ReviewCallBack.new(m.value.cb),
            )
        )
    return kb


def states_to_keyboards(state: TaskStates) -> InlineKeyboardMarkup:
    return {
        state.NEW: get_new_task_menu,
        state.ON_REVIEW: get_review_task_menu,
        state.FIX_REQUIRED: get_task_resubmit_menu,
        state.FINAL_REVIEW_REQUIRED: get_final_tasks_menu,
    }.get(state)()
