class Type:
    def __init__(self, name: str, id: str, interactions: dict):
        self.name = name
        self.id = id
        self.interactions = interactions

class Rock(Type):
    def __init__(self):
        super().__init__("Rock", "rock", {
            "rock": 0,
            "paper": -1,
            "scissors": 0
        })

class Paper(Type):
    def __init__(self):
        super().__init__("Paper", "paper", {
            "rock": 0,
            "paper": 0,
            "scissors": -1
        })

class Scissors(Type):
    def __init__(self):
        super().__init__("Scissors", "scissors", {
            "rock": -1,
            "paper": 0,
            "scissors": 0
        })

class Attack(Type):
    def __init__(self):
        super().__init__("Attack", "attack", {
            "attack": -1,
            "defend": 0,
            "special": -2,
            "deflect": 0,
            "heal": 0
        })

class Defend(Type):
    def __init__(self):
        super().__init__("Defend", "defend", {
            "attack": 0,
            "defend": 0,
            "special": -1,
            "deflect": 0,
            "heal": 0
        })

class Special(Type):
    def __init__(self):
        super().__init__("Special", "special", {
            "attack": -1,
            "defend": -1,
            "special": -2,
            "deflect": -2,
            "heal": 0
        })

class Deflect(Type):
    def __init__(self):
        super().__init__("Deflect", "deflect", {
            "attack": -1,
            "defend": 0,
            "special": 0,
            "deflect": 0,
            "heal": 0
        })

class Heal(Type):
    def __init__(self):
        super().__init__("Heal", "heal", {
            "attack": 0,
            "defend": 1,
            "special": -1,
            "deflect": 1,
            "heal": 1
        })