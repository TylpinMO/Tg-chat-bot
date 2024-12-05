from aiogram import Dispatcher
from aiogram.types import Message
from utils import (
    update_homie_points, 
    generate_stats, 
    create_room, 
    join_room, 
    leave_room, 
    start_game, 
    list_rooms, 
    rooms,
    update_balances,
    next_turn,
    is_game_over
)

def register_handlers(dp: Dispatcher):
    # --- Команды работы с карамельками ---
    @dp.message(commands=["homie"])
    async def homie_handler(message: Message):
        user_id = message.from_user.id
        username = message.from_user.username or message.from_user.first_name

        result = update_homie_points(user_id, username)
        if result is None:
            await message.reply("Ты уже получал карамельки за последние 6 часов. Попробуй позже!")
        else:
            user_points, points_gained = result
            await message.reply(
                f"@{username}, ты получил {points_gained} карамелек. Всего у тебя {user_points} карамелек!"
            )
        await message.delete()

    @dp.message(commands=["statshomie"])
    async def stats_handler(message: Message):
        stats_message = generate_stats()
        await message.reply(stats_message)
        await message.delete()

    # --- Команды для игры в Блэкджек ---
    @dp.message(commands=["blackjack"])
    async def blackjack_handler(message: Message):
        room_id = create_room(message.from_user.id)
        await message.reply(f"Комната #{room_id} создана! Присоединяйтесь с помощью /join {room_id}.")

    @dp.message(commands=["join"])
    async def join_handler(message: Message):
        args = message.text.split()
        if len(args) != 2:
            await message.reply("Укажите ID комнаты: /join [ID комнаты]")
            return

        room_id = args[1]
        user_id = message.from_user.id
        username = message.from_user.username or message.from_user.first_name

        result = join_room(room_id, user_id, username)
        await message.reply(result)

    @dp.message(commands=["leave"])
    async def leave_handler(message: Message):
        user_id = message.from_user.id
        result = leave_room(user_id)
        await message.reply(result)

    @dp.message(commands=["rooms"])
    async def rooms_handler(message: Message):
        rooms_list = list_rooms()
        await message.reply(rooms_list)

    @dp.message(commands=["bet"])
    async def bet_handler(message: Message):
        args = message.text.split()
        if len(args) != 2 or not args[1].isdigit():
            await message.reply("Укажите ставку в карамельках: /bet [ставка]")
            return

        bet = int(args[1])
        user_id = message.from_user.id

        for room_id, room in rooms.items():
            if room.status == "waiting" and user_id in room.players:
                response = room.place_bet(user_id, bet)
                await message.reply(response)
                return

        await message.reply("Вы не подключены к комнате или игра уже началась.")

    @dp.message(commands=["start"])
    async def start_handler(message: Message):
        user_id = message.from_user.id
        for room_id, room in rooms.items():
            if room.owner == user_id and room.status == "waiting":
                response = start_game(room_id)
                await message.reply(response)
                return

        await message.reply("Вы не являетесь создателем комнаты или игра уже началась.")

    @dp.message(commands=["hit"])
    async def hit_handler(message: Message):
        user_id = message.from_user.id
        for room_id, room in rooms.items():
            if room.status == "playing" and room.current_turn == user_id:
                response = room.hit(user_id)
                await message.reply(response)

                if room.players[user_id]["status"] == "busted":
                    room.current_turn = next_turn(room, user_id)
                if is_game_over(room):
                    room.dealer_turn()
                    results = room.determine_results()
                    update_balances(room)
                    room.status = "finished"
                    await message.reply(f"Игра окончена!\n\n{results}")
                return

        await message.reply("Сейчас не ваш ход или вы не участвуете в игре.")

    @dp.message(commands=["stand"])
    async def stand_handler(message: Message):
        user_id = message.from_user.id
        for room_id, room in rooms.items():
            if room.status == "playing" and room.current_turn == user_id:
                response = room.stand(user_id)
                await message.reply(response)

                room.current_turn = next_turn(room, user_id)

                if is_game_over(room):
                    room.dealer_turn()
                    results = room.determine_results()
                    update_balances(room)
                    room.status = "finished"
                    await message.reply(f"Игра окончена!\n\n{results}")
                return

        await message.reply("Сейчас не ваш ход или вы не участвуете в игре.")