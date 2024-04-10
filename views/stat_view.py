import arcade
import arcade.gui
from arcade.gui import UIManager
import math

from views.health import Sprite
from state import State

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FONT_SIZE = 20

SPRITE_SCALING = 3.5
OPPONENT_SPRITE_SCALING = 3

# Button formatting
BUTTON_WIDTH = 175
V_BOX_X = 100
V_BOX_Y = -225
V_BOX_2_X = 300
V_BOX_2_Y = -190

# This PokemonStats view class displays the sprite of the selected pokemon along with their stats relating to
# health, attacking, moves, etc.
class PokemonStats(arcade.View):
    def __init__(self, player, enemy, pokemon, state):
        super().__init__()
        self.pokemon = pokemon
        self.player = player
        self.enemy = enemy
        self.state = state

        # Background image will be stored in this variable
        self.background = None
        arcade.set_background_color(arcade.color.WHITE)

        self.player_list = None

        # Button styling
        button_style = {
            "bg_color":(50,75,125),
            "bg_color_pressed":(20, 65, 115)
        }

        # Create "go back" button
        self.v_box = arcade.gui.UIBoxLayout()
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
            text = str(self.pokemon.get_name())
        )


    def setup(self):
        # Create the sprite for the pokemon to be displayed
        self.player_list = arcade.SpriteList()
        self.player_sprite = Sprite("../cs3050_pokemon/sprites/" + self.pokemon.get_name().lower() + "-front.png")
        self.player_sprite.scale = SCREEN_HEIGHT  / (self.player_sprite.height * 2)


        self.player_sprite.center_x = SCREEN_WIDTH / 4
        self.player_sprite.center_y = 2*SCREEN_HEIGHT /3

        self.player_list.append(self.player_sprite)
        self.name_text.center_x = SCREEN_WIDTH / 4
        self.name_text.center_y = self.player_sprite.bottom - SCREEN_HEIGHT / 30
        self.player_list.append(self.name_text)

        # Stats text output
        self.health_text = arcade.create_text_sprite (
            start_x=SCREEN_WIDTH / 4,
            start_y=SCREEN_HEIGHT / 2,
            color=arcade.color.BLACK,
            text = "Health: " + str(math.trunc(self.pokemon.get_curr_hlth()))
                                    + "\nAttack: " + str(int(self.pokemon.get_curr_atk()))
                                    + "\nDefense: " + str(int(self.pokemon.get_curr_def()))
                                    + "\nSpeed: " + str(int(self.pokemon.get_curr_spd()))
                                    + "\n\nMoves:\n"
                                    + "(1) " + str(self.pokemon.moves[0].name) + " (Power: " + str(int(self.pokemon.moves[0].get_power())) + " and Accuracy: " + str(int(self.pokemon.moves[0].get_accuracy())) + ")"
                                    + "\n(2) " + str(self.pokemon.moves[1].name) + " (Power: " + str(int(self.pokemon.moves[1].get_power())) + " and Accuracy: " + str(int(self.pokemon.moves[1].get_accuracy())) + ")"
                                    + "\n(3) " + str(self.pokemon.moves[2].name) + " (Power: " + str(int(self.pokemon.moves[2].get_power())) + " and Accuracy: " + str(int(self.pokemon.moves[2].get_accuracy())) + ")"
                                    + "\n(4) " + str(self.pokemon.moves[3].name) + " (Power: " + str(int(self.pokemon.moves[3].get_power())) + " and Accuracy: " + str(int(self.pokemon.moves[3].get_accuracy())) + ")"
        )
        self.health_text.center_x = SCREEN_HEIGHT
        self.health_text.center_y = 3*SCREEN_HEIGHT / 4
        self.player_list.append(self.health_text)

    def back_button_action(self, event):
        # switch screen to swapping screen
        if(self.state.get_state().value == State.Stat.value):
            print("returning to swap screen")
            self.state.set_state(State.PokemonSwap)
            self.state.set_rendered(False)
        elif(self.state.get_state().value == State.PartyStat.value):
            print("returning to party screen")
            self.state.set_state(State.Party)
            self.state.set_rendered(False)

    def on_draw(self):
            # Clear the screen
            self.clear()
        
            # Draw all the sprites.
            self.manager.draw()
            self.player_list.draw()

