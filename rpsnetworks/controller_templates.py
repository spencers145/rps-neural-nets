from rpsnetworks.gamestate import *
from rpsnetworks import network
import random

class Controller:
    def __init__(self, id: str, controller_callable):
        self.id = id
        self.controller_callable = controller_callable
    
    def getMove(self, gamestate) -> str:
        return self.controller_callable(gamestate)

class randomController(Controller):
    def __init__(self, id: str):
        super().__init__(id, self.pickRandomMove)
    
    def pickRandomMove(self, gamestate: GameState):
        moves = list(gamestate.allowed_moves.keys())
        rand_int = random.randint(0, len(moves) - 1)
        return moves[rand_int]

class mixedStrategyController(Controller):
    def __init__(self, id: str, strategy: list[float]):
        self.strategy = strategy
        super().__init__(id, self.pickWeightedRandomMove)
    
    def pickWeightedRandomMove(self, gamestate: GameState):
        moves = list(gamestate.allowed_moves.keys())
        return random.choices(moves, self.strategy)[0]

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
        return list(gamestate.allowed_moves.keys())[max_index]

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
        moves = list(gamestate.allowed_moves.keys())
        return random.choices(moves, strategy)[0]

class playerAwareNeuralNetworkController(Controller):
    def __init__(self, id: str, network: network.Network):
        self.network = network
        super().__init__(id, self.pickNeuralNetworkAdvisedMove)
        self.first_turn_memory = {}

    def pickNeuralNetworkAdvisedMove(self, gamestate: GameState):
        if gamestate.turn == 0:
            for i in range(0, len(gamestate.players)):
                self.first_turn_memory[gamestate.players[i].id] = i

        input = [0] * self.network.getInputSize()
        for player in gamestate.players:
            index_into = self.first_turn_memory[player.id]
            input[index_into] = player.hit_points

        for i in range(len(self.first_turn_memory.keys()), self.network.getInputSize()):
            input[i] = random.random()
        
        self.network.updateInputs(input)
        self.network.update()
        output = self.network.readOutput()
        max_output = max(output)
        max_index = output.index(max_output)
        return list(gamestate.allowed_moves.keys())[max_index]