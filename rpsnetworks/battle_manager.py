import json
from rpsnetworks import player_templates, schema_templates
from rpsnetworks.gamestate import *

def dumpPlayersToJSON(players: list[player_templates.Player]) -> str:
    JSON_compatible_players = []
    for player in players:
        JSON_compatible_object = {
            "id": player.ID,
            "hp": player.hit_points,
            "controller_id": player.CONTROLLER.ID
        }
        JSON_compatible_players.append(JSON_compatible_object)
    
    return json.dumps(JSON_compatible_players)

class Game:
    def __init__(self, id: str, players: list[player_templates.Player], schema: schema_templates.Schema, options: dict):
        self.ID = id
        self.SCHEMA = schema
        self.OPTIONS = options
        self.players = players

        # we include this option because not recording players is faster
        if "record_players" in list(options.keys()):
            self.RECORD_PLAYERS = options["record_players"]
        else: self.RECORD_PLAYERS = False

        self.history = []
        self.turn = -1

        self.gameOver = False

        self.validatePlayers()

    def validatePlayers(self):
        for player in self.players:
            assert player.hit_points > 0, "%s has 0 hit points." %(player.id)

    def step(self):
        # if the game is over, don't step
        if self.isGameOver(): return

        # advance the gamestate
        self.turn += 1
        
        # pre-define a dictionary to represent the gamestate
        gamestate = GameState(self.players, self.SCHEMA.TYPES, self.turn, self.history)
        
        # get the moves of each player
        moves = []
        for player in self.players:
            moves.append(player.getMove(gamestate))

        # dump players to json for later use
        if self.RECORD_PLAYERS: players_before_turn = dumpPlayersToJSON(self.players)

        # execute the outcome of each move
        # loop over indices so we can exclude players from executing moves on themselves
        for i in range(0, len(moves)):
            for j in range(0, len(self.players)):
                if i != j:
                    attacking_type = moves[i]
                    defending_type = moves[j]
                    defending_player = self.players[j]
                    
                    health_change = self.SCHEMA.getHealthChange(attacking_type, defending_type)
                    defending_player.changeHealth(health_change)

        # remove defeated players
        self.purgeDefeatedPlayers()

        # update history
        if self.RECORD_PLAYERS: self.updateHistory(players_before_turn, self.players, moves, self.turn)
        else: self.updateHistory("", "", moves, self.turn)

    def purgeDefeatedPlayers(self):
        # iterate backwards through players
        # pop off those who have been defeated
        for i in range(len(self.players) - 1, -1, -1):
            if self.players[i].hit_points == 0:
                self.players.pop(i)

    def updateHistory(self, players_before_turn, players_after_turn, moves, turn):
        gamestate = {
            "players_before_turn": players_before_turn,
            "players_after_turn": dumpPlayersToJSON(players_after_turn),
            "moves": moves,
            "turn": turn
        }

        self.history.append(gamestate)

    def isGameOver(self) -> bool:
        alive_players = 0
        for player in self.players:
            if player.hit_points > 0: alive_players += 1
        
        return alive_players < 2
    
    def getCurrentResults(self) -> list[str]:
        returnable = []
        for player in self.players:
            returnable.append(player.ID)
        return returnable

    def getHistory(self) -> list[dict]:
        return self.history
            

class Manager:
    def __init__(self):
        self.games = {}
        self.history = {}
        self.results = {}

    def newGame(self, id: str, players: list[player_templates.Player], schema: schema_templates.Schema, options: dict):
        self.games[id] = Game(id, players, schema, options)

    def stepAllGamesToCompletion(self):
        steps = 0
        while steps < 99 and len(self.games.keys()) > 0:
            self.stepAllGames()
            steps += 1
    
    def stepGameToCompletion(self, game_id):
        steps = 0
        while steps < 99:
            if self.stepGame(game_id): break
            steps += 1

    def stepAllGames(self):
        # step all games
        for game_id in list(self.games.keys()):
            self.stepGame(game_id)

    def stepGame(self, game_id) -> bool:
        game = self.games[game_id]

        # step game
        game.step()

        # check if game is over
        game_over = game.isGameOver()
        if game_over:
            # if so, remove from our list of games and add its results to our list of results
            self.results[game_id] = game.getCurrentResults()
            self.history[game_id] = game.getHistory()
            del self.games[game_id]
        return game_over
    
    def wipeResults(self):
        self.results = {}

    def wipeHistory(self):
        self.history = {}

def runGames(manager: Manager, number_of_games: int, players: list[player_templates.Player], schema: schema_templates.Schema, options: dict):
    for i in range(0, number_of_games):
        for player in players: player.resetHealth()
        manager.newGame("network_game_%d" %(i), players.copy(), schema, options)
        manager.stepGameToCompletion("network_game_%d" %(i))