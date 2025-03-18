from aiogram import Router, types, F, Bot
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, ReplyKeyboardRemove, BotCommand
from datetime import datetime, timedelta

from humanfriendly.terminal import message
from openpyxl.utils import dataframe
from telebot.types import Message


from db import *
import app.kb as kb
import json


#Создается маршрутизатор
router = Router()

#Состояния для FSM
class Registration(StatesGroup):
    waiting_for_contact = State()
    waiting_for_day = State()


# Загрузка JSON файла
with open("/Users/admin/Documents/Python_projects/Schedule_bot_for_TUIT/database/translation.json", "r", encoding="utf-8") as f:
    translations = json.load(f)

# Функция для получения перевода
def get_text(key, lang="ru"):
    return translations.get(key, {}).get(lang, key) # Если ключа нет то вернет сам key

# Команды с описанием
async def set_bot_commands(bot: Bot):
    commands = [
        BotCommand(command="/start", description="Открытие бота, настройка"),
        BotCommand(command="/time", description="Время занятий"),
        BotCommand(command="/info", description="Информация о боте"),
        BotCommand(command="/help", description="Помощь")
    ]
    await bot.set_my_commands(commands) # Передаем список команд

# Создаем клавиатуру для выбора языка
user_languages = {}

# handler для команды start
@router.message(Command("start"))
async def command_start(msg: types.Message, state: FSMContext):
    await msg.answer(f'Добро пожаловать, {msg.from_user.first_name}.\n'
                     f'Выберите язык:\nTilni tanlang:',
                     reply_markup=kb.language_keyboard)


# команда для помощи
@router.message(Command('help'))
async def get_help(msg: types.Message):
    await msg.answer(text = "Это бот для расписания преподавателей!")


# команда для выбора языка и отправки телефон номера для проверки
@router.message(lambda msg: msg.text in ["🇷🇺 Русский язык", "🇺🇿 O'zbek tili"])
async def language_selected(msg: types.Message):
    user_id = msg.from_user.id
    if msg.text == "🇷🇺 Русский язык":
        user_languages[user_id] = "ru"
        await msg.answer("Вы выбрали русский язык. 🇷🇺\n"
                         "Пожалуйста отправьте телефон номер для проверки",
                         reply_markup=kb.get_number_keyboard())
    else:
        user_languages[user_id] = "uz"
        await msg.answer("Siz o'zbek tilini tanladingiz. 🇺🇿\n"
                         "Iltimos, Telefon raqamingizni jonating",
                         reply_markup=kb.get_number_keyboard())



# handler для получения номер телефона
@router.message(lambda msg: msg.contact is not None)
async def check_phone(msg: types.Message, state: FSMContext):
    user_id = msg.from_user.id
    lang = user_languages.get(user_id, "ru")
    user_phone = normalize_phone(msg.contact.phone_number)

    if is_teacher_registered(user_phone):
        await msg.answer(get_text("choose_schedule", lang),
                         reply_markup=kb.schedule_keyboard())

    else:
        await msg.answer(get_text("not_registered", lang),
                         reply_markup=ReplyKeyboardRemove())


# команда для выбора дня расписания
@router.message(lambda msg: msg.text in translations["days_button"]["ru"] + translations["days_button"]["uz"])
async def handle_schedule_choice(msg: types.Message):
    user_id = msg.from_user.id
    lang = user_languages.get(user_id, "ru")
    if msg.text == translations["days_button"]:
        # Замените на логику для сегодняшнего расписания
        await msg.answer(translations["today's_schedule_answer"])
    elif msg.text == translations["days_button"]:
        # Замените на логику для завтрашнего расписания
        await msg.answer(translations["tomorrow's_schedule_answer"])
    elif msg.text == translations["days_button"]:
        await msg.answer(
            translations["weekly's_schedule_answer"],
            reply_markup=kb.days_keyboard()
        )


def get_schedule_for_day(date):
    day_of_week = date.strftime("%A")

    # Перевод на русский язык
    days_ru = {
        "Monday": "Понедельник",
        "Tuesday": "Вторник",
        "Wednesday": "Среда",
        "Thursday": "Четверг",
        "Friday": "Пятница",
        "Saturday": "Суббота",
        "Sunday": "Воскресенье"
    }
    day_of_week = days_ru[day_of_week]

    #Фильтруем расписание по дню недели
    filtered = df[df["день недели"] == day_of_week]

    if filtered.empty:
        return 'Расписание не найдено'

    result = f'Расписание на {day_of_week}:\n\n'
    for _, row in filtered.iterrows():
        result += f"🕒 {row['Нумерация пар']}: {row['Название предмета']} ({row['Номер аудитории']})\n"

    return result


# Handler для выбора дня недели
@router.message(lambda msg: msg.text in ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"])
async def handle_day_choice(msg: types.Message):
    await msg.answer(f"Вот расписание на {msg.text.lower()}:")

# Handler для кнопки "Назад"
@router.message(lambda msg: msg.text == "Назад")
async def handle_back_button(msg: types.Message):
    await msg.answer(
        "Выберите тип расписания:",
        reply_markup=kb.schedule_keyboard()
    )

