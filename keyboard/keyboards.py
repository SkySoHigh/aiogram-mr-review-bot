from enum import Enum

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboard.callbacks import ReviewCallBack, MenuCallBack
from locales import Locale


class MainMenu(str, Enum):
    send_tasks_to_pm = Locale.Menu.SHOW_USER_TASKS_BTN
    send_tasks_to_group_chat = Locale.Menu.SHOW_ALL_TASKS_BTN
    show_adm_menu = Locale.Menu.SHOW_ADM_MENU_BTN


class TaskMenuOnReview(str, Enum):
    take = Locale.Task.TAKE_BTN


class TaskMenuFinalReview(str, Enum):
    submitted = Locale.Task.SUBMIT_BTN


class TaskMenuReviewFinished(str, Enum):
    confirmed = Locale.Task.CONFIRMED_BTN
    canceled = Locale.Task.REJECT_BTN


def get_tasks_on_review_menu():
    kb = InlineKeyboardMarkup()
    for m in TaskMenuOnReview:
        kb.add(InlineKeyboardButton(text=m, callback_data=ReviewCallBack.new(m)))
    return kb


def get_tasks_submitted_menu():
    kb = InlineKeyboardMarkup()
    for m in TaskMenuFinalReview:
        kb.add(InlineKeyboardButton(text=m, callback_data=ReviewCallBack.new(m)))
    return kb


def get_tasks_confirmation_menu():
    kb = InlineKeyboardMarkup()
    for m in TaskMenuReviewFinished:
        kb.add(InlineKeyboardButton(text=m, callback_data=ReviewCallBack.new(m)))
    return kb


def get_main_menu():
    kb = InlineKeyboardMarkup()
    for m in MainMenu:
        kb.add(InlineKeyboardButton(text=m, callback_data=MenuCallBack.new(m)))
    return kb
