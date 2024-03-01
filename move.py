from enum import Enum

Type = Enum("Type", ["Normal", "Fire", "Water", "Electric", "Grass", "Ice", "Fighting", "Poison", "Ground", "Flying", "Psychic", "Bug", "Rock", "Ghost", "Dragon", "Dark", "Steel"])

class move:
    
    """
    constructor for move
    name - name of move - string
    description - description of move - string
    power - numeric power of move - int
    accuracy - numeric accuracy of move from 0 - 100 - int
    type - type of move - Type enum
    is_atk - bool whether or not move is an attacking move
    """
    def __init__(self, name, description, power, accuracy, type, is_atk):
        self.name = name
        self.description = description
        self.power = power
        self.accuracy = accuracy
        self.type = type
        self.is_atk = is_atk

    #getters
    def get_name(self):
        return self.name
    
    def get_description(self):
        return self.description
    
    def get_power(self):
        return self.power
    
    def get_accuracy(self):
        return self.accuracy
    
    def get_type(self):
        return self.type

    def get_is_atk(self):
        return self.is_atk





    

    