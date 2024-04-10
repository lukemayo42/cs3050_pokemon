import move
class stat_mod_move(move):
    '''
    move subclass - move that will alter stats of a pokemon instead of attack pokemon
    name - name of move - string
    description - description of move - string
    power - numeric power of move - int
    accuracy - numeric accuracy of move from 0 - 100 - int
    type - type of move - Type enum
    is_atk - bool whether or not move is an attacking move
    stat_to_mod - string - what stat the move will change
    raise_or_lower - bool - true if move will raise attacking pokemons stats, false if pokemon will lower opponets pokemon stats
    level - int - 1 or 2 - level of stat modifier - can stack up to 6
        - raise stat
            - 1st - 50%, 1.5x- 2nd - 100%, 2x - 3rd - 150%, 2.5x - 4th - 200%, 3X - 5th - 250%, 3.5x - 6th - 300% - 4x
        - lower stat
            - 1st - 33%, .66x - 2nd, 50%, .5 - 3rd - 60% , .4x - 4th- 66.6%, .33x - 5th - 71.5%, .285x - 6th - 75%, .25%
    '''
    def __init__(self, name, description, type, is_atk, stat_to_mod, raise_self_or_lower_enemy, stat_level_change):
        super().__init__(name, description, 0, 100, type, is_atk)
        self.stat_to_mod = stat_to_mod
        self.raise_or_lower = raise_self_or_lower_enemy
        self.level = stat_level_change

    #getters
    def get_stat_to_mod(self):
        return self.stat_to_mod
    
    def get_raise_or_lower(self):
        return self.raise_or_lower
    
    def get_level(self):
        return self.level
    

    def modify_pokemon(self, pokemon):
        if self.raise_or_lower:
            #raise pokemons stats
            #if self.
            pass
        else:
            #lower pokemons stats
            pass
        

    def modify_stat(self, pokemon):
        pass