import item_objects
class Character:
    """
    Constructor for character class
    name: name of character {string}
    pokemon_list:  List of pokemon the player has {list}
    item_bag: Dictionary that contains items {Dictionary}
    money: amount of money the character has {integer}
    speech_bubble_text: text that is said/shows up in speech bubble when approached {string}
    prev_pkm_index: holds the index of the previous pokemon that was out, -1 if no prev pkm
    """
    def __init__(self, name, pokemon_list, item_bag, money, speech_bubble_text):
        self.name = name
        self.pokemon_list = pokemon_list
        self.item_bag = item_bag
        self.money = money
        self.speech_bubble_text = speech_bubble_text
        self.prev_pkm_index = -1

    def display_character_info(self):
        print(f"Name: {self.name}")
        print(f"Pokemon List: {self.pokemon_list}")
        print(f"Item Bag: {self.item_bag}")
        print(f"Money: {self.money}")
        print(f"Speech Bubble Text: {self.speech_bubble_text}")

    # Getters
    def get_name(self):
        return self.name

    def get_pokemon_list(self):
        return self.pokemon_list

    def get_item_bag(self):
        return self.item_bag

    def get_money(self):
        return self.money

    def get_speech_bubble_text(self):
        return self.speech_bubble_text

    # Function gets the current first pokemon in the pokemon list
    def get_curr_pkm(self):
        return self.pokemon_list[0]
    
    def get_prev_pkm(self):
        return self.prev_pkm_index

    # Setters
    def set_name(self, value):
        self.name = value

    def set_pokemon_list(self, value):
        self.pokemon_list = value

    def set_item_bag(self, value):
        self.item_bag = value

    def set_money(self, value):
        self.money = value

    def set_speech_bubble_text(self, value):
        self.speech_bubble_text = value

    def set_prev_pkm_index(self):
        self.prev_pkm_index = -1

    # Function adds a pokemon to the players pokemon list
    def add_pokemon(self, pokemon):
        self.pokemon_list.append(pokemon)

    # Function removes a pokemon to the players pokemon list
    def remove_pokemon(self, pokemon):
        for i in range(len(self.pokemon_list)):
            if self.pokemon_list[i] == pokemon:
                self.pokemon_list.remove(i)

    #removes all pokemon from characters party
    def remove_all_pokemon(self):
        self.pokemon_list = []



    # Function that allows user to reorder the list of pokemon they have
    def swap_pokemon(self, pokemon1_index, pokemon2_index):
        pokemon_temp = self.pokemon_list[pokemon1_index]
        self.pokemon_list[pokemon1_index] = self.pokemon_list[pokemon2_index]
        self.pokemon_list[pokemon2_index] = pokemon_temp
        self.prev_pkm_index = pokemon1_index


    # Function that adds an item to a characters item_list
    def add_item(self, item, amount):
        if item in self.item_bag:
            self.item_bag[item] += amount
        else:
            self.item_bag[item] = amount

    # Function that adds an item to a characters item_list
    def remove_item(self, item, amount):
        if item in self.item_bag:
            if self.item_bag[item] <= amount:
                del self.item_bag[item]
            else:
                self.item_bag[item] -= amount

    # Function Checks to see how many of an item the character has, and returns that number
    def amount_of_item(self, trainer_item):
        for item in self.item_bag:
            if item == trainer_item:
                return self.item_bag[item]

    # Function that updates the characters money
    def add_money(self, amount):
        self.money += amount

    # Function that updates the characters money
    def subtract_money(self, amount):
        self.money -= amount
        if self.money < 0:
            self.money = 0

    # Function checks the list of pokemon the character has to make sure they still have a pokemon with health
    # returns true if there is a non fainted pokemon left in the party otherwise false
    def chk_party(self):
        valid = False
        for pkm in self.pokemon_list:
            if not pkm.get_is_fainted():
                valid = True
        return valid
    
    #heals all pokemon in the characters party and resets is_fainted back to false, and resets items 
    def reset(self):
        for pkm in self.pokemon_list:
            pkm.set_is_fainted(False)
            pkm.set_curr_hlth(pkm.get_max_hlth())
        self.items = {item_objects.potion: 1, item_objects.super_potion: 1, item_objects.hyper_potion: 1,
                      item_objects.max_potion: 1}

    
        
