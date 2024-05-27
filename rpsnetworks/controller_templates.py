from rpsnetworks.gamestate import *
from rpsnetworks import network
import random

class Controller:
    def __init__(self, id: str, controller_callable):
        self.ID = id
        self.CONTROLLER_CALLABLE = controller_callable
    
    def getMove(self, gamestate) -> str:
        return self.CONTROLLER_CALLABLE(gamestate)

class randomController(Controller):
    def __init__(self, id: str):
        super().__init__(id, self.pickRandomMove)
    
    def pickRandomMove(self, gamestate: GameState):
        moves = list(gamestate.ALLOWED_MOVES.keys())
        rand_int = random.randint(0, len(moves) - 1)
        return moves[rand_int]

class mixedStrategyController(Controller):
    def __init__(self, id: str, strategy: list[float]):
        self.strategy = strategy
        super().__init__(id, self.pickWeightedRandomMove)
    
    def pickWeightedRandomMove(self, gamestate: GameState):
        moves = list(gamestate.ALLOWED_MOVES.keys())
        return random.choices(moves, self.strategy)[0]

# designed for RPG Fascimile
class customStrategy1Controller(Controller):
    def __init__(self, player_id: str, id: str, strategy: list[float]):
        self.strategy = strategy
        self.PLAYER_ID = player_id
        super().__init__(id, self.pickWeightedRandomMove)
    
    def pickWeightedRandomMove(self, gamestate: GameState):
        strategy_this_turn = self.strategy.copy()
        # find myself
        for player in gamestate.PLAYERS:
            if player.ID == self.PLAYER_ID:
                myself = player
                break
        
        # strategic AI
        another_same = False
        another_at_1 = False
        another_at_2 = False
        for player in gamestate.PLAYERS:
            if player.ID != self.PLAYER_ID:
                another_same = another_same or player.hit_points == myself.hit_points
                another_at_1 = another_at_1 or player.hit_points == 1
                another_at_2 = another_at_2 or player.hit_points == 2
        
        if another_at_1:
            # kill!!!
            strategy_this_turn[0] *= 4
        
        if another_at_2:
            # win in sight
            strategy_this_turn[0] *= 2
            strategy_this_turn[2] *= 2

        if myself.hit_points == 1:
            # defending isn't going to help
            strategy_this_turn[1] *= 0
            if not another_at_1:
                # attacking doesn't win
                strategy_this_turn[0] *= 0
            if not another_at_2:
                # specialing doesn't win
                strategy_this_turn[2] *= 0
        elif myself.hit_points == 2:
            # let's not get specialed
            strategy_this_turn[3] *= 3
            strategy_this_turn[4] *= 4
        else:
            # offensive plays are good
            strategy_this_turn[0] *= 3
            strategy_this_turn[2] *= 2
            if another_same:
                # don't let them take the health advantage
                strategy_this_turn[4] *= 3
            
        moves = list(gamestate.ALLOWED_MOVES.keys())
        return random.choices(moves, strategy_this_turn)[0]


class basicNeuralNetworkController(Controller):
    def __init__(self, id: str, network: network.Network):
        self.network = network
        super().__init__(id, self.pickNeuralNetworkAdvisedMove)

    def pickNeuralNetworkAdvisedMove(self, gamestate: GameState):
        input = []
        # note to self: make this not suck
        for i in range(0, self.network.getInputSize()):
            input.append(random.random())
        self.network.updateInputs(input)
        self.network.update()
        output = self.network.readOutput()
        max_output = max(output)
        max_index = output.index(max_output)
        return list(gamestate.ALLOWED_MOVES.keys())[max_index]

class probabilisticNeuralNetworkController(Controller):
    def __init__(self, id: str, network: network.Network):
        self.network = network
        super().__init__(id, self.pickNeuralNetworkAdvisedMove)

    def pickNeuralNetworkAdvisedMove(self, gamestate: GameState):
        input = []
        # note to self: make this not suck
        for i in range(0, self.network.getInputSize()):
            input.append(random.random())
        self.network.updateInputs(input)
        self.network.update()
        strategy = self.network.readOutput()
        for i in range(0, len(strategy)):
            if strategy[i] < 0: strategy[i] = 0
        moves = list(gamestate.ALLOWED_MOVES.keys())
        return random.choices(moves, strategy)[0]

class playerAwareNeuralNetworkController(Controller):
    def __init__(self, id: str, network: network.Network):
        self.network = network
        super().__init__(id, self.pickNeuralNetworkAdvisedMove)
        self.first_turn_memory = {}

    def pickNeuralNetworkAdvisedMove(self, gamestate: GameState):
        if gamestate.TURN == 0:
            for i in range(0, len(gamestate.PLAYERS)):
                self.first_turn_memory[gamestate.PLAYERS[i].ID] = i

        input = [0] * self.network.getInputSize()
        for player in gamestate.PLAYERS:
            index_into = self.first_turn_memory[player.ID]
            input[index_into] = player.hit_points

        for i in range(len(self.first_turn_memory.keys()), self.network.getInputSize()):
            input[i] = random.random()
        
        self.network.updateInputs(input)
        self.network.update()
        output = self.network.readOutput()
        max_output = max(output)
        max_index = output.index(max_output)
        return list(gamestate.ALLOWED_MOVES.keys())[max_index]