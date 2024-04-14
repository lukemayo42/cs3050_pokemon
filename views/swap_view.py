import arcade
import arcade.gui
from arcade.gui import UIManager
from battle import battle
import math

from views.health import Sprite
from state import State

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FONT_SIZE = 20
TOP_ROW = 2 * SCREEN_HEIGHT / 3 + (SCREEN_HEIGHT / 8)
BOTTOM_ROW = SCREEN_HEIGHT / 3 + (SCREEN_HEIGHT / 8)

SPRITE_SCALING = 3.5
OPPONENT_SPRITE_SCALING = 3

# Button formatting
BUTTON_WIDTH = 175
V_BOX_X = 100
V_BOX_Y = -225
V_BOX_2_X = 300
V_BOX_2_Y = -190

# This PokemonSwap view class gives the fighter a chance to switch between all of the pokemon in their party during the fight.
class PokemonSwap(arcade.View):
    def __init__(self, player, enemy, state):
        super().__init__()
        self.player = player
        self.enemy = enemy
        self.pokemon = player.get_curr_pkm()
        self.state = state

        # This variable keeps track of what pokemon you are looking at
        self.index = 0

        # Background image will be stored in this variable
        self.background = None
        arcade.set_background_color(arcade.color.WHITE)

        self.player_list = None


        # Button styling
        button_style = {
            "bg_color":(50,75,125),
            "bg_color_pressed":(20, 65, 115)
        }

        # Create "go back" button if the pokemon hasn't fainted
        self.v_box = arcade.gui.UIBoxLayout()
        if(not self.player.get_curr_pkm().get_is_fainted()):
            back_button = arcade.gui.UIFlatButton(text="Go Back", width=BUTTON_WIDTH * .75, style=button_style)
            self.v_box.add(back_button.with_space_around(bottom=20))

            # Assign self.items_button as a callback to render item bag
            back_button.on_click = self.back_button_action

        self.manager = UIManager()
        self.manager.enable()
        # Create a widget to hold the v_box widget, that will center the buttons
        self.manager.add(
            arcade.gui.UIAnchorWidget(align_x=-SCREEN_WIDTH / 3, align_y= -SCREEN_HEIGHT / 2.5,
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box)
        )
        # Add name/stats for pokemon
        self.name_text = arcade.create_text_sprite (
            start_x=SCREEN_WIDTH / 4,
            start_y=SCREEN_HEIGHT / 2,
            color=arcade.color.BLACK,
            text = str(self.pokemon.get_name()) +
                    "\nHealth: " + str(math.trunc(self.player.get_curr_pkm().get_curr_hlth()))
                                    + "\nAttack: " + str(int(self.pokemon.get_curr_atk()))
                                    + "\nDefense: " + str(int(self.pokemon.get_curr_def()))
                                    + "\nSpeed: " + str(int(self.pokemon.get_curr_spd()))
                                    + "\n\nMoves:\n"
                                    + "(1) " + str(self.player.get_curr_pkm().moves[0].name) + " (Power: " + str(int(self.player.get_curr_pkm().moves[0].get_power())) + " and Accuracy: " + str(int(self.player.get_curr_pkm().moves[0].get_accuracy())) + ")"
                                    + "\n(2) " + str(self.player.get_curr_pkm().moves[1].name) + " (Power: " + str(int(self.player.get_curr_pkm().moves[1].get_power())) + " and Accuracy: " + str(int(self.player.get_curr_pkm().moves[1].get_accuracy())) + ")"
                                    + "\n(3) " + str(self.player.get_curr_pkm().moves[2].name) + " (Power: " + str(int(self.player.get_curr_pkm().moves[2].get_power())) + " and Accuracy: " + str(int(self.player.get_curr_pkm().moves[2].get_accuracy())) + ")"
                                    + "\n(4) " + str(self.player.get_curr_pkm().moves[3].name) + " (Power: " + str(int(self.player.get_curr_pkm().moves[3].get_power())) + " and Accuracy: " + str(int(self.player.get_curr_pkm().moves[3].get_accuracy())) + ")"
        )

    def setup(self):
        # Create sprites for swap page
        self.background_sky = arcade.load_texture("../cs3050_pokemon/images/screen_background.png")
        self.player_list = arcade.SpriteList()
        self.player_sprite = Sprite("../cs3050_pokemon/sprites/" + self.player.get_curr_pkm().get_name().lower() + "-front.png", SPRITE_SCALING)
        self.player_sprite.center_x = SCREEN_WIDTH / 4
        self.player_sprite.center_y = 3 * SCREEN_HEIGHT / 4

        self.player_list.append(self.player_sprite)
        self.name_text.center_x = SCREEN_WIDTH / 4
        self.name_text.center_y = self.player_sprite.bottom - self.name_text.height / 2
        self.player_list.append(self.name_text)
        self.pokemon_list = self.player.get_pokemon_list()
        # Iterate through pokemon party and display other sprites on the side
        for pokemon in self.pokemon_list:
            print(pokemon.get_name())
        for i in range(1, len(self.pokemon_list)):
                # Add the sprite image to the list of sprites to render
                sprite = Sprite("../cs3050_pokemon/sprites/" + self.pokemon_list[i].get_name().lower() + "-front.png")
                sprite.scale = SCREEN_HEIGHT / (self.player_sprite.height * 1.2)

                sprite.center_x = SCREEN_HEIGHT
                if( i == 1):
                    sprite.center_y = 2 * SCREEN_WIDTH / 3.2
                else:
                    sprite.center_y = SCREEN_WIDTH / 3.2
                self.player_list.append(sprite)

                # Add the pokemon name to the list of sprites to render
                name = arcade.create_text_sprite (
                    start_x=SCREEN_HEIGHT,
                    start_y=i * SCREEN_WIDTH / 3.2,
                    color=arcade.color.BLACK,
                    text = str(self.pokemon_list[i].get_name())
                )
                name.center_x = SCREEN_HEIGHT
                name.center_y = sprite.bottom - SCREEN_HEIGHT / 30

                self.player_list.append(name)
                if(i == 1):
                    self.create_pokemon_buttons(SCREEN_HEIGHT, .85 * TOP_ROW, True, self.pokemon_list[i].get_is_fainted())
                else:
                    self.create_pokemon_buttons(SCREEN_HEIGHT,  BOTTOM_ROW / 2, False, self.pokemon_list[i].get_is_fainted())                    
            
        print("here is your pokemon party")

    def back_button_action(self, event):
        # switch screen to fighting screen
        if(self.state.get_state().value == State.PokemonSwap.value):
            print("returning to fight screen")
            self.state.set_state(State.Battle)
            self.state.set_rendered(False)

    def create_pokemon_buttons(self, pos_x, pos_y, top, fainted):
        # Create the option to swap to the pokemon if it hasn't fainted and to see stats
        if(top):
            self.button_box_1 = arcade.gui.UIBoxLayout(vertical=False)

            stats_button = arcade.gui.UIFlatButton(text="Stats", width=BUTTON_WIDTH / 2)
            self.button_box_1.add(stats_button.with_space_around(left=20))
            stats_button.on_click = self.generate_stats_view_1

            if(not fainted):
                swap_button = arcade.gui.UIFlatButton(text="Swap", width=BUTTON_WIDTH / 2)
                self.button_box_1.add(swap_button.with_space_around(left=20))
                swap_button.on_click = self.swap_action_1
            # Create widgets to hold the button_box_1 widgets, that will center the buttons
            # self.manager.add(
            #     arcade.gui.UIAnchorWidget(align_x=pos_x / 3, align_y=pos_y,
            #         anchor_x="center_x",
            #         anchor_y="center_y",
            #         child=self.button_box_1)
            # )
            self.manager.add(
                arcade.gui.UIAnchorWidget(align_x=pos_x / 3, align_y=(pos_y - (SCREEN_HEIGHT / 20)) - SCREEN_HEIGHT / 2,
                    anchor_x="center_x",
                    anchor_y="center_y",
                    child=self.button_box_1)
            )

        else:
            self.button_box_2 = arcade.gui.UIBoxLayout(vertical=False)
            stats_button = arcade.gui.UIFlatButton(text="Stats", width=BUTTON_WIDTH / 2)
            self.button_box_2.add(stats_button.with_space_around(left=20))
            stats_button.on_click = self.generate_stats_view_2

            if(not fainted):
                swap_button = arcade.gui.UIFlatButton(text="Swap", width=BUTTON_WIDTH / 2)
                self.button_box_2.add(swap_button.with_space_around(left=20))
                swap_button.on_click = self.swap_action_2

            # Create widgets to hold the button_box_2 widgets, that will center the buttons
            self.manager.add(
                arcade.gui.UIAnchorWidget(align_x=pos_x / 3, align_y=(pos_y - (SCREEN_HEIGHT / 20)) - SCREEN_HEIGHT / 2,
                    anchor_x="center_x",
                    anchor_y="center_y",
                    child=self.button_box_2)
            )
    def generate_stats_view_1(self, event):
        self.index = 1
        self.state.set_user_choice(self.index)
        self.generate_stats()

    def swap_action_1(self, event):
        self.index = 1
        self.state.set_user_choice(self.index)
        self.swap_pokemon()

    def generate_stats_view_2(self, event):
        self.index = 2
        self.state.set_user_choice(self.index)
        self.generate_stats()

    def swap_action_2(self, event):
        self.index = 2
        self.state.set_user_choice(self.index)
        self.swap_pokemon()

    def generate_stats(self):
        # Get the selected pokemon and pass it to the stats view
        pokemon = self.player.get_pokemon_list()[self.index]
        if(self.state.get_state().value == State.PokemonSwap.value):
            print("going to stats screen")
            self.state.set_state(State.Stat)
            self.state.set_rendered(False)

    def swap_pokemon(self):
        # Call backend method to swap the pokemon order so that the first pokemon is back in front
        # Return to the battle screen
        state_switched = False
        if(not self.player.get_curr_pkm().get_is_fainted()):
            btn_info = ["swap", self.index]
            player_action, enemy_action, action_list = battle(self.player, self.enemy, btn_info)
            self.state.set_action_list(action_list)
            if(player_action != "fainted" and self.state.get_state().value == State.PokemonSwap.value):
                self.state.set_state(State.Wait)
                self.state.set_rendered(False)
                state_switched = True
                print("returning to battle screen")
            elif(self.state.get_state().value == State.PokemonSwap.value):
                # Force the swap and then return to fight
                self.state.set_state(State.Wait)
                self.state.set_rendered(False)
        elif not state_switched:
            self.player.swap_pokemon(0, self.index)
            self.state.add_new_action(["player", "swap", f"{self.player.get_name()} swapped out {self.player.get_pokemon_list()[self.index].get_name()} with {self.player.get_curr_pkm().get_name()}"])
            self.state.set_state(State.Wait)
            self.state.set_rendered(False)

    def on_draw(self):
        # Clear the screen
        self.clear()
        arcade.draw_lrwh_rectangle_textured(0, 0,
                                        SCREEN_WIDTH, SCREEN_HEIGHT,
                                        self.background_sky)
        # Draw all the sprites.
        self.manager.draw()
        self.player_list.draw()