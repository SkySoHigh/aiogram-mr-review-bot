from enum import Enum

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pydantic import BaseModel

from common import callbacks
from locales import Locale


class TextToCallback(BaseModel):
    text: str
    cb: str


class GroupMainMenu(Enum):
    send_tasks_to_pm = TextToCallback(text=Locale.Menu.SHOW_USER_TASKS_BTN, cb='send_task_t_pm')
    send_tasks_to_group_chat = TextToCallback(text=Locale.Menu.SHOW_ALL_TASKS_BTN, cb='send_active_tasks_to_chat')
    show_adm_menu = TextToCallback(text=Locale.Menu.SHOW_ADM_MENU_BTN, cb='send_active_tasks_to_pm')


class PmMainMenu(Enum):
    get_all_user_tasks = TextToCallback(text=Locale.Menu.SHOW_USER_TASKS_BTN, cb='get_all_user_tasks')


class TaskMenuOnReview(Enum):
    take = TextToCallback(text=Locale.Task.TAKE_BTN, cb='take_task')


class TaskMenuFinalReview(Enum):
    submitted = TextToCallback(text=Locale.Task.SUBMIT_BTN, cb='submit_task')


class TaskMenuReviewFinished(Enum):
    confirmed = TextToCallback(text=Locale.Task.CONFIRMED_BTN, cb='confirm_task')
    rejected = TextToCallback(text=Locale.Task.REJECT_BTN, cb='reject_task')


def get_tasks_on_review_menu():
    kb = InlineKeyboardMarkup()
    for m in TaskMenuOnReview:
        kb.add(InlineKeyboardButton(text=m.value.text, callback_data=callbacks.ReviewCallBack.new(m.value.cb)))
    return kb


def get_tasks_submitted_menu():
    kb = InlineKeyboardMarkup()
    for m in TaskMenuFinalReview:
        kb.add(InlineKeyboardButton(text=m.value.text, callback_data=callbacks.ReviewCallBack.new(m.value.cb)))
    return kb


def get_tasks_confirmation_menu():
    kb = InlineKeyboardMarkup()
    for m in TaskMenuReviewFinished:
        kb.add(InlineKeyboardButton(text=m.value.text, callback_data=callbacks.ReviewCallBack.new(m.value.cb)))
    return kb


def get_main_menu_for_group():
    kb = InlineKeyboardMarkup()
    for m in GroupMainMenu:
        kb.add(InlineKeyboardButton(text=m.value.text, callback_data=callbacks.MenuCallBack.new(m.value.cb)))
    return kb

def get_main_menu_for_pm():
    kb = InlineKeyboardMarkup()
    for m in PmMainMenu:
        kb.add(InlineKeyboardButton(text=m.value.text, callback_data=callbacks.MenuCallBack.new(m.value.cb)))
    return kb

