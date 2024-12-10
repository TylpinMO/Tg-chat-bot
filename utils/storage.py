import json
import os
from datetime import datetime, timedelta

ROOMS = {} # Хранение всех активных комнат

DATA_FILE = "user_data.json"

def create_room(room_id, creator_id):
    """Создает новую комнату для игры."""
    ROOMS[room_id] = {
        "players": {creator_id: {"balance": 0, "hand": [], "bet": 0}},
        "creator": creator_id,
        "started": False,
    }
    return ROOMS[room_id]

def get_room(room_id):
    """Получает данные комнаты."""
    return ROOMS.get(room_id)

def join_room(room_id, player_id):
    """Добавляет игрока в комнату."""
    room = get_room(room_id)
    if room:
        if room["started"]:
            return False
        if len(room["players"]) >= 4:
            return False
        room["players"][player_id] = {"balance": 0, "hand": [], "bet": 0}
        return True
    return False

def leave_room(room_id, player_id):
    """Удаляет игрока из комнаты."""
    room = get_room(room_id)
    if room:
        room["players"].pop(player_id, None)
        if not room["players"]: #Удаляем комнату, если она пустая
            ROOMS.pop(room_id)
        return True
    return False

def list_rooms():
    """Возвращает список активных комнат."""
    return [
        {"room_id": room_id, "players": len(ROOMS[room_id]["players"]), "max_players": 4}
        for room_id in ROOMS if not ROOMS[room_id]["started"]
    ]

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
        data[str(user_id)] = {
            "balance": 0,
            "last_points": None,
            "games_played": 0,
            "wins": 0,
            "losses": 0,
            "ties": 0,
        }
        save_data(data)
    return data[str(user_id)]

def update_user_data(user_id, balance=None, last_points=None, games_played=None, wins=None, losses=None, ties=None):
    """Обновляет данные пользователя."""
    data = load_data()
    if str(user_id) in data:
        if balance is not None:
            data[str(user_id)]["balance"] = balance
        if last_points is not None:
            data[str(user_id)]["last_points"] = last_points
        if games_played is not None:
            data[str(user_id)]["games_played"] = games_played
        if wins is not None:
            data[str(user_id)]["wins"] = wins
        if losses is not None:
            data[str(user_id)]["losses"] = losses
        if ties is not None:
            data [str(user_id)]["ties"] = ties
        save_data(data)