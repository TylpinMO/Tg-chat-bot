import json
from datetime import datetime, timedelta
import random

DATA_FILE = "data.json"
DATA_FILE = "homie_data.json"
rooms = {}

def load_data():
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file)

def update_homie_points(user_id, username=None, delta=0):
    """
    Обновляет карамельки для пользователя. Если delta != 0, изменяет баланс.
    """
    data = load_data()
    user = data.get(str(user_id), {"username": username or "Unknown", "points": 0})
    if delta != 0:
        user["points"] += delta
    if username:
        user["username"] = username  # Обновляем имя пользователя
    data[str(user_id)] = user
    save_data(data)
    return user["points"]

def generate_stats():
    data = load_data()
    leaderboard = sorted(data.items(), key=lambda x: x[1]["points"], reverse=True)[:10]
    statuses = [
        "Король Нахаловки", "Зам. короля", "Смотрящий", "Хоуми", 
        "Большой брат", "Младший брат", "Пупуня", 
        "Убежище", "Попуск", "Пять курица"
    ]
    stats = ["Стата мужиков на районе:"]
    for index, (user_id, user_data) in enumerate(leaderboard, start=1):
        username = user_data["username"]
        status = statuses[index - 1] if index <= len(statuses) else "Новичок"
        points = user_data["points"]
        stats.append(f"{index}. {status} - @{username} - {points} карамелек")
    return "\n".join(stats)

def initialize_data():
    global rooms
    try:
        with open(DATA_FILE, "r") as file:
            data = json.load(file)
            rooms.update(data.get("rooms", {}))
    except FileNotFoundError:
        save_data()

def save_data():
    with open(DATA_FILE, "w") as file:
        json.dump({"rooms": rooms}, file)

def create_room(chat_id, host_id):
    room_id = random.randint(1000, 9999)
    rooms[room_id] = {
        "chat_id": chat_id,
        "host_id": host_id,
        "players": {},
        "status": "waiting",
        "game": None
    }
    save_data()
    return room_id

from game import BlackjackGame

rooms = {}

def create_room(chat_id, host_id):
    room_id = random.randint(1000, 9999)
    while room_id in rooms:
        room_id = random.randint(1000, 9999)
    rooms[room_id] = BlackjackGame(room_id, host_id)
    return room_id

def join_room(room_id, user_id, username):
    if room_id not in rooms:
        return "Комната не найдена."
    room = rooms[room_id]
    if room.status != "waiting":
        return "Невозможно подключиться. Игра уже началась."
    room.add_player(user_id, username)
    return f"@{username} присоединился к комнате {room_id}!"

def start_game(host_id):
    for room_id, room in rooms.items():
        if room.host_id == host_id and room.status == "waiting":
            if len(room.players) < 2:
                return "Для начала игры требуется минимум 2 игрока."
            room.status = "playing"
            room.deal_initial_cards()
            return "Игра началась! Карты розданы. Ход первого игрока."
    return "Вы не являетесь создателем комнаты или комната уже занята."
  
def next_turn(room, current_user_id):
    """
    Возвращает ID следующего игрока. Если все игроки завершили, возвращает None.
    """
    player_ids = list(room.players.keys())
    current_index = player_ids.index(current_user_id)
    for i in range(1, len(player_ids) + 1):
        next_index = (current_index + i) % len(player_ids)
        if room.players[player_ids[next_index]]["status"] == "playing":
            return player_ids[next_index]
    return None

def is_game_over(room):
    """
    Проверяет, завершили ли все игроки свои ходы.
    """
    return all(player["status"] != "playing" for player in room.players.values())

def update_balances(room):
    """
    Обновляет карамельки игроков после завершения игры.
    """
    dealer_score = room.dealer["score"]
    for player_id, player in room.players.items():
        if player["status"] == "busted":
            # Игрок проиграл — ставка сгорает
            continue
        elif player["score"] > dealer_score or dealer_score > 21:
            # Игрок выиграл — x2 ставки
            update_homie_points(player_id, None, delta=player["bet"] * 2)
        elif player["score"] == dealer_score:
            # Ничья — ставка возвращается
            update_homie_points(player_id, None, delta=player["bet"])
        else:
            # Игрок проиграл — ставка сгорает
            continue
# Список комнат
rooms = {}

def leave_room(user_id):
    """
    Функция для выхода игрока из комнаты.
    Если игрок - создатель комнаты, она удаляется.
    """
    for room_id, room in rooms.items():
        if user_id in room.players:
            # Удаляем игрока из списка игроков
            room.players.remove(user_id)
            
            if room.owner == user_id:
                # Если игрок был владельцем, удаляем комнату
                del rooms[room_id]
                return f"Комната #{room_id} удалена, так как создатель покинул её."
            
            return f"Вы покинули комнату #{room_id}."
    
    return "Вы не находитесь в комнате."
  
def list_rooms():
    """
    Функция для вывода всех доступных комнат.
    """
    if not rooms:
        return "Нет доступных комнат."
    
    room_list = ["Доступные комнаты:"]
    for room_id, room in rooms.items():
        status = "Ожидание игроков" if room.status == "waiting" else "Игра идет"
        room_list.append(f"Комната #{room_id} - {status} (Владельцы: {room.owner}, Игроки: {len(room.players)})")
    return "\n".join(room_list)