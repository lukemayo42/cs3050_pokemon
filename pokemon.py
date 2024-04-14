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
    """
    #define multiple contructors
    def __init__(self, *args):
        #copy contructor called if 1 argument is passed to contructor
        if len(args) == 1:
            self.name = args[0].get_name()
            self.types = args[0].get_types()
            self.moves = args[0].get_moves()
            self.max_hlth = args[0].get_max_hlth()
            self.curr_hlth = args[0].get_max_hlth()
            self.base_atk = args[0].get_base_atk()
            self.curr_atk = args[0].get_base_atk()
            self.base_def = args[0].get_base_def()
            self.curr_def = args[0].get_base_def()
            self.base_spd = args[0].get_base_spd()
            self.curr_spd = args[0].get_base_spd()
            self.is_fainted = False
            self.atk_mod = 0
            self.def_mod = 0
            self.spd_mod = 0
            self.prev_hlth = self.get_max_hlth()
            self.hlth_after_move = self.get_max_hlth()
            self.hlth_after_item = self.get_max_hlth()
        #regular contructor takes 7 arguments
        elif len(args) == 7:
            self.name = args[0]
            self.types = args[1]
            self.moves = args[2]
            self.max_hlth = args[3]
            self.curr_hlth = args[3]
            self.base_atk = args[4]
            self.curr_atk = args[4]
            self.base_def = args[5]
            self.curr_def = args[5]
            self.base_spd = args[6]
            self.curr_spd = args[6]
            self.is_fainted = False
            self.atk_mod = 0
            self.def_mod = 0
            self.spd_mod = 0
            self.prev_hlth = self.get_max_hlth()
            self.hlth_after_move = self.get_max_hlth()
            self.hlth_after_item = self.get_max_hlth()
   
    '''
    def __init__(self, pkm):
        self.name = pkm.get_name()
        self.types = pkm.get_types()
        self.moves = pkm.get_moves()
        self.max_hlth = pkm.get_max_hlth()
        self.curr_hlth = pkm.get_max_hlth()
        self.base_atk = pkm.get_base_atk()
        self.curr_atk = pkm.get_base_atk()
        self.base_def = pkm.get_base_def()
        self.curr_def = pkm.get_base_def()
        self.base_spd = pkm.get_base_spd()
        self.curr_spd = pkm.get_base_spd()
        self.is_fainted = False
'''

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
    
    def get_atk_mod(self):
        return self.atk_mod
    
    def get_def_mod(self):
        return self.def_mod

    def get_spd_mod(self):
        return self.spd_mod
    
    def get_prev_hlth(self):
        return self.prev_hlth
    
    def get_hlth_after_move(self):
        return self.hlth_after_move
    
    def get_hlth_after_item(self):
        return self.hlth_after_item
    #setters
    def set_curr_hlth(self, new_hlth):
        self.curr_hlth = new_hlth
    
    def set_curr_atk(self, new_atk):
        self.curr_atk = new_atk

    def set_curr_def(self, new_def):
        self.curr_def = new_def

    def set_curr_spd(self, new_spd):
        self.curr_spd = new_spd

    def set_is_fainted(self, new_is_fainted):
        self.is_fainted = new_is_fainted

    def set_moves(self, moves):
        self.moves = moves

    def set_atk_mod(self, mod):
        self.atk_mod = mod

    def set_def_mod(self, mod):
        self.def_mod = mod

    def set_spd_mod(self, mod):
        self.spd_mod = mod

    def set_prev_hlth(self, prev_hlth):
        self.prev_hlth = prev_hlth

    def set_hlth_after_move(self, new_hlth):
        self.hlth_after_move = new_hlth
    
    def set_hlth_after_item(self, new_hlth):
        self.hlth_after_item = new_hlth


    #add health and remove health functions
    def add_health(self, hlth):
        #self.prev_hlth = self.curr_hlth
        self.curr_hlth += hlth
        if self.curr_hlth > self.max_hlth:
            self.curr_hlth = self.max_hlth
        
        

    def remove_health(self, hlth):
        #self.prev_hlth = self.curr_hlth
        self.curr_hlth -= hlth
        if self.curr_hlth < 0:
            self.curr_hlth = 0
            self.is_fainted = True
            
        self.set_hlth_after_move(self.get_curr_hlth())


    #print functions!!!! - need to know how gui wants text info

    def move_to_string(self, move_used, hit, effectiveness, crit, character):
        return_string = ""
        if hit:
            if effectiveness == 1:
                return_string = f"{character.get_name()}'s {self.name} used {move_used.get_name()}"
            elif effectiveness == .5 or effectiveness == .25:
                return_string =  f"{character.get_name()}'s {self.name} used {move_used.get_name()}. It's not very effective."
            elif effectiveness == 2 or effectiveness == 4:
                return_string =  f"{character.get_name()}'s {self.name} used {move_used.get_name()}. It's Super Effective!"
            elif effectiveness == 0:
                return f"{character.get_name()}'s {self.name} used {move_used.get_name()}. It had no effect"
            if crit == 2:
                return_string += " It's a Critical Hit!"
            return return_string
        else:
            return f"{character.get_name()}'s {self.name}'s move missed"
    
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
    

    

    

    
    

    