# this file exists only for organizational reasons
class GameState:
    def __init__(self, players: list, allowed_moves: dict, turn: int, history: list[dict]):
        self.players = players
        self.allowed_moves = allowed_moves
        self.turn = turn
        self.history = history