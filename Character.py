import arcade
class Character:
    """
    Constructor for character class
    name: name of character {string}
    pokemon_list:  List of pokemon the player has {list}
    item_bag: Dictionary that contains items {Dictionary}
    money: amount of money the character has {integer}
    speech_bubble_text: text that is said/shows up in speech bubble when approached {string}
    """
    def __init__(self, name, pokemon_list, item_bag, money, speech_bubble_text):
        self.name = name
        self.pokemon_list = pokemon_list
        self.item_bag = item_bag
        self.money = money
        self.speech_bubble_text = speech_bubble_text

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

    def money(self):
        return self.money

    def get_speech_bubble_text(self):
        return self.speech_bubble_text

    # Function gets the current first pokemon in the pokemon list
    def get_curr_pkm(self):
        return self.pokemon_list[0]

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

    # Function adds a pokemon to the players pokemon list
    def add_pokemon(self, pokemon):
        self.pokemon_list.append(pokemon)

    # Function adds a pokemon to the players pokemon list
    def remove_pokemon(self, pokemon):
        for i in range(len(self.pokemon_list)):
            if self.pokemon_list[i] == pokemon:
                self.pokemon_list.remove(i)

    # Function that allows user to reorder the list of pokemon they have
    def swap_pokemon(self, pokemon1_index, pokemon2_index):
        pokemon_temp = self.pokemon_list[pokemon1_index]
        self.pokemon_list[pokemon1_index] = self.pokemon_list[pokemon2_index]
        self.pokemon_list[pokemon2_index] = pokemon_temp


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
