from rpsnetworks import controller_templates, network

class Player:
    def __init__(self, id: str, maximum_hit_points: int, controller: controller_templates.Controller):
        self.ID = id
        self.MAXIMUM_HIT_POINTS = maximum_hit_points
        self.CONTROLLER = controller
        self.resetHealth()

    def getMove(self, gamestate) -> str:
        return self.CONTROLLER.getMove(gamestate)

    def changeHealth(self, amount):
        self.hit_points += amount
        if self.hit_points < 0: self.hit_points = 0
    
    def resetHealth(self):
        self.hit_points = self.MAXIMUM_HIT_POINTS

class randomPlayer(Player):
    def __init__(self, id: str, maximum_hit_points: int):
        super().__init__(id, maximum_hit_points, controller_templates.randomController("random"))
    
class mixedStrategyPlayer(Player):
    def __init__(self, id: str, maximum_hit_points: int, strategy: list[float]):
        super().__init__(id, maximum_hit_points, controller_templates.mixedStrategyController("random", strategy))

class basicNetworkPlayer(Player):
    def __init__(self, id: str, maximum_hit_points: int, controller_id: str, network: network.Network):
        super().__init__(id, maximum_hit_points, controller_templates.basicNeuralNetworkController(controller_id, network))
        
class probabilisticNetworkPlayer(Player):
    def __init__(self, id: str, maximum_hit_points: int, controller_id: str, network: network.Network):
        super().__init__(id, maximum_hit_points, controller_templates.probabilisticNeuralNetworkController(controller_id, network))

class playerAwareNetworkPlayer(Player):
    def __init__(self, id: str, maximum_hit_points: int, controller_id: str, network: network.Network):
        super().__init__(id, maximum_hit_points, controller_templates.playerAwareNeuralNetworkController(controller_id, network))