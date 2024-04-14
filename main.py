import arcade
import arcade.gui
from Character import Character
import pokemon_objects as pkm_obj
import item_objects

from views.start import PokemonStart
from views.world import WorldMap, Gym
from views.fight_view import PokemonGame
from views.move_view import PokemonMove
from views.swap_view import PokemonSwap
from views.stat_view import PokemonStats
from views.items_view import PokemonItem
from views.choose_party_view import PokemonParty
from views.end_battle import EndBattle
from views.char_selection_view import PlayerSelectView
from views.waiting_view import Waiting
import state
from state import State

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
W_SCREEN_TITLE = "Pokemon World"
B_SCREEN_TITLE = "Battle"

#TODO: figure out waiting
#right now we are wiating in the fight_view may want to make wait own view
#idea: create different views on different waits - damage wait, fainted wait, swapping wait - some of these may be able to be in one view beacuse we just need to display text
# send over list(or dictionary) of strings that will need to be displayed as text, would be 2 or three strings
# based on list or dictionary determines what wait to do and we will display text, will need to wait multiple times to diplay text
#need to do different thing on each wait, change user/enemy health, faint, swap  - make single view for waiting, take in value for text to be dislpayed and action that needs to happen, as well as the current state of the battle, and the number of actions that need to happen and the current action that the wait is on
#what we need to do this - strings with the action text in them - strings saying what action is in each string - number of actions to be displayed - current action 

# Pokemon is a python arcade window that renders the views from the directory and updates the rendering
# as the views change the state of the game.
class Pokemon(arcade.Window):
    def __init__(self, width, height, title, player, enemy, state):
        super().__init__(width, height, title)
        self.state = state
        self.player = player
        self.enemy = enemy
        self.pokemon_bag_user = [pkm_obj.pikachu, pkm_obj.charizard, pkm_obj.bulbasaur, 
                                 pkm_obj.pidgeotto, pkm_obj.gengar, pkm_obj.butterfree, 
                                 pkm_obj.slowbro, pkm_obj.lucario, pkm_obj.wooper]


        # Background image will be stored in this variable
        self.background = None

    # Check states set by individual views and update rendering
    def on_update(self, delta_time):
        # print(self.state.get_state())
        if(check_render(self.state, State.Start)):
            print("rendering")
            self.state.set_rendered(True)
            start_view = PokemonStart(self.player, self.enemy, self.state)
            self.show_view(start_view)
            start_view.setup()
        if(check_render(self.state, State.CharacterSelect)):
            print("choosing character")
            self.state.set_rendered(True)
            character_view = PlayerSelectView(self.player, self.state)
            self.show_view(character_view)
        if(check_render(self.state, State.Party) or check_render(self.state, State.Party2)):
            print("choose party")
            self.state.set_rendered(True)
            choose_view = PokemonParty(self.player, self.enemy, self.pokemon_bag_user, self.state)
            self.show_view(choose_view)
            choose_view.setup()
        if(check_render(self.state, State.World)):
            print("entering the world")
            self.state.set_rendered(True)
            map_view = WorldMap(self.player, self.enemy, self.state)
            map_view.setup()
            self.show_view(map_view)
        if(check_render(self.state, State.Gym)):
            gym_view = Gym(self.player, self.enemy, self.state)
            gym_view.setup()
            self.show_view(gym_view)
        if(check_render(self.state, State.Battle)):
            print("battle")
            self.state.set_rendered(True)
            fight_view = PokemonGame(self.player, self.enemy, self.state)
            fight_view.setup()
            self.show_view(fight_view)
        if(check_render(self.state, State.Moves)):
            print("moves")
            self.state.set_rendered(True)
            moves_view = PokemonMove(self.player, self.enemy, self.state)
            moves_view.setup()
            self.show_view(moves_view)
        if(check_render(self.state, State.PokemonSwap)):
            print("swapping")
            self.state.set_rendered(True)
            swap_view = PokemonSwap(self.player, self.enemy, self.state)
            swap_view.setup()
            self.show_view(swap_view)
        if(check_render(self.state, State.Stat)):
            print("stats")
            self.state.set_rendered(True)
            stat_view = PokemonStats(self.player, self.enemy, self.player.get_pokemon_list()[self.state.get_user_choice()], self.state)
            stat_view.setup()
            self.show_view(stat_view)
        if(check_render(self.state, State.PartyStat)):
            print("stats")
            self.state.set_rendered(True)
            stat_view = PokemonStats(self.player, self.enemy, self.pokemon_bag_user[self.state.get_user_choice()], self.state)
            stat_view.setup()
            self.show_view(stat_view)
        if(check_render(self.state, State.PartyStat2)):
            print("stats")
            self.state.set_rendered(True)
            stat_view = PokemonStats(self.player, self.enemy, self.pokemon_bag_user[self.state.get_user_choice()], self.state)
            stat_view.setup()
            self.show_view(stat_view)
        if(check_render(self.state, State.Item)):
            print("items")
            self.state.set_rendered(True)
            item_view = PokemonItem(self.player, self.enemy, self.state)
            item_view.setup()
            self.show_view(item_view)
        if(check_render(self.state, State.Win)):
            print("won")
            self.state.set_rendered(True)
            reset_characters([self.player, pkm_obj.gym_leader, pkm_obj.youngster_joey, pkm_obj.team_rocket_member, pkm_obj.ace_trainer, self.enemy])
            self.player.remove_all_pokemon()
            start_view = EndBattle(self.player, self.enemy, self.state)
            start_view.setup()
            self.show_view(start_view)
        if(check_render(self.state, State.Loss)):
            print("loss")
            self.state.set_rendered(True)
            reset_characters([self.player, pkm_obj.gym_leader, pkm_obj.youngster_joey, pkm_obj.team_rocket_member, pkm_obj.ace_trainer, self.enemy])
            self.player.remove_all_pokemon()
            start_view = EndBattle(self.player, self.enemy, self.state)
            start_view.setup()
            self.show_view(start_view)
        if(check_render(self.state, State.Wait)):
            print("wait")
            self.state.set_rendered(True)
            start_view = Waiting(self.player, self.enemy, self.state)
            start_view.setup()
            self.show_view(start_view)

# Helper function to act as an overloaded operator and confirm the screen needs to be rendered
def check_render(state, check_state):
    if(state.get_state().value == check_state.value and not state.get_rendered()):
        return True
    else:
        return False

#hepler function to reset all character objects after winning/losing to play again
# takes in character objects as a list
def reset_characters(objects_list):
    for character in objects_list:
        character.reset()
    
# This main function creates two pokemon bags, two Character objects, and passes them
# to the PokemonGame object and renders the window to run the game.
def main():
    """ Main function """
    pokemon_bag_user = [pkm_obj.pikachu, pkm_obj.charizard, pkm_obj.bulbasaur]
    user_item_bag = {item_objects.potion: 1, item_objects.super_potion: 1, item_objects.hyper_potion: 1,
                        item_objects.max_potion: 1}
    pokemon_bag_user_2 = []
    

    pokemon_bag_enemy = [pkm_obj.enemy_charizard, pkm_obj.enemy_gengar, pkm_obj.enemy_pidgeotto]
    enemy_item_bag = {item_objects.potion: 1, item_objects.super_potion: 1, item_objects.hyper_potion: 1,
                      item_objects.max_potion: 1}

    user_trainer = Character("Ash", pokemon_bag_user_2, user_item_bag, 1000,
                              "I'm on a journey to become a Pokemon Master!")
    enemy_trainer = Character("Misty", pokemon_bag_enemy, enemy_item_bag, 800, "Water types are the best!")

    game_view = Pokemon(SCREEN_WIDTH, SCREEN_HEIGHT, B_SCREEN_TITLE, user_trainer, enemy_trainer, state.game_state)
    arcade.run()

if __name__ == "__main__":
    main()


