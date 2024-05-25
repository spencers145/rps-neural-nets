from importlib import reload
from type_templates import *

class Schema: 
    def __init__(self, name: str, id: str, types: list[Type]):
        self.name = name
        self.id = id

        # add our types as a dictionary
        self.types = self.generateTypeKey(types)
        
        # make sure our types have defined interactions
        self.validateTypes()
    
    def validateTypes(self):
        for type_id in self.types:
            # get all keys in the first's type interactions
            type = self.types[type_id]
            interaction_keys = type.interactions.keys()

            for comparison_type_id in self.types:
                # ensure the two compared types have a defined interaction
                assert comparison_type_id in interaction_keys, "Invalid schema. %s (offensive) interaction with %s (defensive) is not defined." %(comparison_type_id, type.id)

    def generateTypeKey(self, types):
        key = {}
        for type in types:
            key[type.id] = type
        return key

    def getHealthChange(self, attacking_type, defending_type):
        return self.types[defending_type].interactions[attacking_type]

class rockPaperScissors(Schema):
    def __init__(self):
        super().__init__("Rock Paper Scissors", "rps", [Rock(), Paper(), Scissors()])

class RPGFascimile(Schema):
    def __init__(self):
        super().__init__("RPG Fascimile", "rpgf", [Attack(), Defend(), Special(), Deflect(), Heal()])

#class randomSchema(Schema):
#    def __init__(self, name: str, id: str, type_names: list[str]):
#        
#        super().__init__(name, id, types)