import json
import os
from datetime import datetime, timedelta

DATA_FILE = "user_data.json"

def load_data():
    """Загружает данные из JSON-файла."""
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)

def save_data(data):
    """Сохраняет данные в JSON-файл."""
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def get_user_data(user_id):
    """Возвращает данные пользователя или создает новый профиль."""
    data = load_data()
    if str(user_id) not in data:
        data[str(user_id)] = {"balance": 0, "last_points": None}
        save_data(data)
    return data[str(user_id)]

def update_user_data(user_id, balance=None, last_points=None):
    """Обновляет данные пользователя."""
    data = load_data()
    if str(user_id) in data:
        if balance is not None:
            data[str(user_id)]["balance"] = balance
        if last_points is not None:
            data[str(user_id)]["last_points"] = last_points
        save_data(data)