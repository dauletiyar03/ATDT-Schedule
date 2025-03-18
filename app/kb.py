import json
from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove,
                           InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from app.handlers import user_languages


with open("/Users/admin/Documents/Python_projects/Schedule_bot_for_TUIT/database/translation.json", "r", encoding="utf-8") as f:
    translations = json.load(f)

def get_text(key, lang="ru"):
    return translations.get(key, {}).get(lang, key)


language_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🇷🇺 Русский язык"), KeyboardButton(text="🇺🇿 O'zbek tili")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

# Клавиатура для отправки номера
def get_number_keyboard(lang) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.button(text=get_text("send_phone", lang), request_contact=True)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)

# Клавиатура для выбора расписания
def schedule_keyboard(lang) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard = [
            [KeyboardButton(text=get_text("today_schedule", lang)),
            KeyboardButton(text=get_text("tomorrow_schedule", lang)),
            KeyboardButton(text=get_text("weekly_schedule", lang))]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

# клавиатуры для дней недели
def days_keyboard(lang="ru") -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
        [KeyboardButton(text=get_text("monday", lang)), KeyboardButton(text=get_text("tuesday", lang))],
        [KeyboardButton(text=get_text("wednesday", lang)), KeyboardButton(text=get_text("thursday", lang))],
        [KeyboardButton(text=get_text("Friday", lang)), KeyboardButton(text=get_text("Saturday", lang))],
        [KeyboardButton(text=get_text("the_back_button", lang))]
        ]
    )
