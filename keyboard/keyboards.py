from enum import Enum

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboard.callbacks import ReviewCallBack, MenuCallBack
from locales import Locale


class MainMenu(str, Enum):
    get_tasks = Locale.Menu.SHOW_TASKS_BTN
    show_adm_menu = Locale.Menu.SHOW_ADM_MENU_BTN


class TaskMenuOnReview(str, Enum):
    take = Locale.NewTaskOnReview.TAKE_NEW_TASK_BTN


class TaskMenuConfirmed(str, Enum):
    confirmed = Locale.TaskConfirmed.CONFIRMED_TASK_BTN


def get_tasks_on_review_menu():
    kb = InlineKeyboardMarkup()
    for m in TaskMenuOnReview:
        kb.add(InlineKeyboardButton(text=m, callback_data=ReviewCallBack.new(m)))
    return kb


def get_tasks_submitted_menu():
    kb = InlineKeyboardMarkup()
    for m in TaskMenuConfirmed:
        kb.add(InlineKeyboardButton(text=m, callback_data=ReviewCallBack.new(m)))
    return kb


def get_main_menu():
    kb = InlineKeyboardMarkup()
    for m in MainMenu:
        kb.add(InlineKeyboardButton(text=m, callback_data=MenuCallBack.new(m)))
    return kb
