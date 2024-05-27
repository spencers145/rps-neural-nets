# this file exists only for organizational reasons
class GameState:
    def __init__(self, players: list, allowed_moves: dict, turn: int, history: list[dict]):
        self.PLAYERS = players
        self.ALLOWED_MOVES = allowed_moves
        self.TURN = turn
        self.HISTORY = history