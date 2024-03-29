class pokemon:

    """
    constructor for pokemon class 
    attributes of class
    name - name of pokemon - string
    types - types of pokemon - list of strings - should type be own class?
    moves - list of move objects 
    max_hlth - max health of pokemon - int
    curr_hlth - current health of pokemon - int
    base_atk - base attack stat of pokemon - int
    curr_atk - current attack of the pokemon - int
    base_def - base defense stat of the pokemon - int
    curr_def - curr defense stat of the pokemon - int 
    base_spd - base speed of the pokemon - int
    curr_spd - current spd of the pokemon - int
    is_fainted - flag whether or not  a pokemon is faineted or not - bool
    """
    def __init__(self, name, types, moves, max_hlth, base_atk, base_def, base_spd):
        #current stats are set to base stats 
        self.name = name
        self.types = types
        self.moves = moves
        self.max_hlth = max_hlth
        self.curr_hlth = max_hlth
        self.base_atk = base_atk
        self.curr_atk = base_atk
        self.base_def = base_def
        self.curr_def = base_def
        self.base_spd = base_spd
        self.curr_spd = base_spd
        self.is_fainted = False

    #getters
    def get_name(self):
        return self.name
    
    def get_types(self):
        return self.types
    
    def get_moves(self):
        return self.moves
    
    def get_max_hlth(self):
        return self.max_hlth
    
    def get_curr_hlth(self):
        return self.curr_hlth
    
    def get_base_atk(self):
        return self.base_atk
    
    def get_curr_atk(self):
        return self.curr_atk
    
    def get_curr_def(self):
        return self.curr_def
    
    def get_base_def(self):
        return self.base_def
    
    def get_base_spd(self):
        return self.base_spd
    
    def get_curr_spd(self):
        return self.curr_spd
    
    def get_is_fainted(self):
        return self.is_fainted
    
    def get_curr_pkm(self):
        return self.pokemon[0]
    
    #setters
    def set_curr_hlth(self, new_hlth):
        self.curr_hlth = new_hlth
    
    def set_curr_atk(self, new_atk):
        self.curr_atk = new_atk

    def set_curr_def(self, new_def):
        self.curr_def = new_def

    def set_curr_spd(self, new_spd):
        self.curr_spd = new_spd

    #add health and remove health functions
    def add_health(self, hlth):
        self.curr_hlth += hlth
        if self.curr_hlth > self.max_hlth:
            self.curr_hlth = self.max_hlth

    def remove_health(self, hlth):
        self.curr_hlth -= hlth
        if self.curr_hlth < 0:
            self.curr_hlth = 0
            self.is_fainted = True


    #print functions!!!! - need to know how gui wants text info

    def move_to_string(self, move_used, hit):
        if hit:
            return f"{self.name} used {move_used.get_name()}"
        else:
            return f"{self.name}'s move missed"
        return move_str
    
    '''
    def get_move_names(self):
        move_str_list = []
        for move in self.moves:
            move_str_list = []
         '''  

    #after wrting move class - write method to get names of moves in list instead of just returning list
    
    
    #attack takes in another pokemon and the pokemons move, and does damage to the pokemon, 
    #take in pokemon as reference to orignal object and do damage to that pokemon
    #might not work becuase you may have to specify the move
    #have to write move class before writing this method
    def attack(enemy_pokemon, move):
        enemy_def = enemy_pokemon.get_curr_def()
        
        pass

    #may want to move out of pokemon class
    #takes in 
    #def calculate_damage(user_atk, enemy_def, move_power)
    

    

    

    
    

    