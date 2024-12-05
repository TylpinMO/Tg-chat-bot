import random

class BlackjackGame:
    def __init__(self, room_id, host_id):
        self.room_id = room_id
        self.host_id = host_id
        self.players = {}
        self.deck = self.generate_deck()
        self.dealer = {"hand": [], "hidden_card": True}
        self.current_turn = None

    def generate_deck(self):
        ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        suits = ["♠️", "♥️", "♣️", "♦️"]
        return [f"{rank}{suit}" for rank in ranks for suit in suits]

    def draw_card(self):
        return self.deck.pop(random.randint(0, len(self.deck) - 1))
      
class BlackjackGame:
    def __init__(self, room_id, host_id):
        self.room_id = room_id
        self.host_id = host_id
        self.players = {}
        self.deck = self.generate_deck()
        self.dealer = {"hand": [], "score": 0, "hidden_card": True}
        self.current_turn = None
        self.status = "waiting"  # "waiting", "playing", "finished"

    def generate_deck(self):
        ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        suits = ["♠️", "♥️", "♣️", "♦️"]
        deck = [f"{rank}{suit}" for rank in ranks for suit in suits]
        random.shuffle(deck)
        return deck

    def calculate_score(self, hand):
        values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 
                  '10': 10, 'J': 10, 'Q': 10, 'K': 10, 'A': 11}
        score = 0
        aces = 0
        for card in hand:
            rank = card[:-1]  # Убираем масть карты
            score += values[rank]
            if rank == 'A':
                aces += 1
        while score > 21 and aces:
            score -= 10
            aces -= 1
        return score

    def add_player(self, user_id, username):
        if user_id not in self.players:
            self.players[user_id] = {
                "username": username,
                "hand": [],
                "score": 0,
                "bet": 0,
                "status": "waiting"  # "waiting", "playing", "busted", "stand"
            }

    def deal_initial_cards(self):
        for player_id in self.players:
            self.players[player_id]["hand"] = [self.deck.pop(), self.deck.pop()]
            self.players[player_id]["score"] = self.calculate_score(self.players[player_id]["hand"])
        self.dealer["hand"] = [self.deck.pop(), self.deck.pop()]
        self.dealer["score"] = self.calculate_score([self.dealer["hand"][0]])

    def hit(self, user_id):
        player = self.players[user_id]
        card = self.deck.pop()
        player["hand"].append(card)
        player["score"] = self.calculate_score(player["hand"])
        if player["score"] > 21:
            player["status"] = "busted"
            return f"@{player['username']}, вы вытянули {card}. Ваш счёт: {player['score']} — перебор!"
        return f"@{player['username']}, вы вытянули {card}. Ваш счёт: {player['score']}."

    def stand(self, user_id):
        player = self.players[user_id]
        player["status"] = "stand"
        return f"@{player['username']} остановился с результатом {player['score']}."

    def dealer_turn(self):
        self.dealer["hidden_card"] = False
        while self.dealer["score"] < 17:
            card = self.deck.pop()
            self.dealer["hand"].append(card)
            self.dealer["score"] = self.calculate_score(self.dealer["hand"])

    def determine_results(self):
        results = []
        dealer_score = self.dealer["score"]
        for player_id, player in self.players.items():
            if player["status"] == "busted":
                results.append(f"@{player['username']} проиграл. Ставка сгорела.")
            elif player["score"] > dealer_score or dealer_score > 21:
                results.append(f"@{player['username']} победил с {player['score']}! Получил x2 ставки.")
            elif player["score"] == dealer_score:
                results.append(f"@{player['username']} сыграл вничью. Ставка возвращена.")
            else:
                results.append(f"@{player['username']} проиграл. Ставка сгорела.")
        return "\n".join(results)