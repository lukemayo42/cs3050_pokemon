from enum import Enum

# Enum to hold the current state of the game, used to update the screen rendering
class State(Enum):
    Start = 1
    World = 2
    Battle = 3
    Moves = 4
    Win = 5
    PokemonSwap = 6
    Bag = 7
    Loss = 8
    Item = 10
    Stat = 11
    Rules = 12
    Gym = 13
    End = 14
    Party = 15
    PartyStat = 16
    CharacterSelect = 17
    Party2 = 18
    PartyStat2 = 19
    Wait = 20

# GameState object to store information about the current state of the game
class GameState:
    def __init__(self, state):
        self.state = state
        self.rendered = False
        self.user_choice = 0
        self.character_sprite = ''
        self.action_list = []
    def get_state(self):
        return self.state
    def get_rendered(self):
        return self.rendered
    def get_user_choice(self):
        return self.user_choice
    def get_character_sprite(self):
        return self.character_sprite
    def get_action_list(self):
        return self.action_list
    def set_action_list(self, new_list):
        self.action_list = new_list
    def add_new_action(self, value):
        self.action_list.append(value)
    def set_state(self, state):
        self.state = state
    def set_rendered(self, rendered):
        self.rendered = rendered
    def set_user_choice(self, user_choice):
        self.user_choice = user_choice
    def set_character_sprite(self, character):
        self.character_sprite = character
    def remove_from_action_list(self):
        self.action_list.pop(0)


# State object used in main
game_state = GameState(State.Start)