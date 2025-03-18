import sqlite3
from dataclasses import Field, replace
from fileinput import filename


import pandas as pd


df = pd.read_excel("/Users/admin/Documents/Python_projects/Schedule_bot_for_TUIT/database/schedule.xlsx")

def is_teacher_registered(phone_number, file_path="/Users/admin/Documents/Python_projects/Schedule_bot_for_TUIT/database/schedule.xlsx"):
    try:
        dif = pd.read_excel(file_path, engine="openpyxl") # Загружаем Excel
        dif = dif.dropna(subset=["Номер телефона"])  # Убираем пустые строки

        teacher_numbers = set(dif["Номер телефона"].
                              astype(str)
                              .str.replace(".0", "", regex=False)
                              .str.replace("+", "", regex=False)
                              .str.strip())
        phone_number = str(phone_number).replace("+", "").strip()

        print(f"Телефон из сообщения: {phone_number}")
        print(f"Телефоны из базы: {teacher_numbers}")

        return phone_number in teacher_numbers # Проверяем есть ли номер
    except FileNotFoundError:
        print("⚠️ Файл расписания не найден!")
        return False
    except KeyError:
        print("⚠️ В Excel нет колонки 'Номер телефона'!")
        return False

def normalize_phone(phone):
    if phone is None:
        return None
    if isinstance(phone, str): # Проверяем, является ли phone строкой
        return phone.replace("+", "").strip() # Удаляем "+" и лишние пробелы
    else: return phone # Если phone не строка, возвращаем как есть

