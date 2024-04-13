import arcade
from arcade import load_texture
import arcade.gui
from arcade.gui import UIManager
from arcade.gui.widgets import UITextArea, UITexturePane

from views.health import HealthBar
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


# This PokemonGame class is created with two trainers passed in, the player and the enemy trainer
# the pokemon bags of each trainer are represented on the screen with Sprites and health_bar sprites.
class Waiting(arcade.View):
    """
    constructor for PokemonGame class
    attributes of class
    width - width of the screen in pixels - int
    height - heigth of the screen in pixels - int
    title - the name of the screen - string
    player - Character object representing the player - Character
    enemy - Character object representing the enemy trainer - Character
    wait - boolean whether game is waiting or not
    """

    def __init__(self, player, enemy, state):
        super().__init__()
        # Start in the battle state for deliverable 1
        self.state = state
        self.player = player
        self.enemy = enemy
        self.action_list = state.get_action_list()
        print(self.action_list)
        self.total_time = 0.0

        # Background image will be stored in this variable
        self.background = None

        # TODO: FOR TESTING PURPOSES, this overrides the original health of the pokemon object
        # self.player.get_curr_pkm().set_curr_hlth(1000)

        # Health bar
        self.bar_sprite_list = arcade.SpriteList()
        self.enemy_health_bar = HealthBar(self.enemy.get_curr_pkm(), self.bar_sprite_list, 350, 500, 515, False)
        self.player_health_bar = HealthBar(self.player.get_curr_pkm(), self.bar_sprite_list, 550, 250, 265, False)

        # ANIMATIONS (future deliverables)
        self.move_up = False
        self.animate = False
        self.background2 = None

        # Variables that will hold sprite lists
        self.player_list = None
        self.enemy_list = None

        # Set up the player info
        self.player_sprite = None

        # Track the current state of what key is pressed (movement for later deliverables)
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        ############ TEXT BOX (just a background for now)
        self.manager = UIManager()
        self.manager.enable()
        bg_tex = load_texture(":resources:gui_basic_assets/window/grey_panel.png")
        self.text_area = UITextArea(x=0,
                                    y=0,
                                    width=SCREEN_WIDTH,
                                    height=SCREEN_HEIGHT / 4,
                                    text= self.action_list[0][2],
                                    font_size=FONT_SIZE,
                                    text_color=arcade.color.BLACK)
        self.manager.add(
            UITexturePane(
                self.text_area.with_space_around(right=20),
                tex=bg_tex,
                padding=(10, 10, 10, 10)
            )
        )

    # This setup method is called when creating all the sprites to be stored on the screen when the window is rendered
    def setup(self):
        """ Set up the game and initialize the variables. """
        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()

        # Set up the player and enemy sprites
        # if the enemy is in the waiting state and pokemon has been swapped render previous pokemon until out of waiting state
        self.player_sprite = Sprite(
            "../cs3050_pokemon/sprites/" + self.player.get_curr_pkm().get_name().lower() + "-back.png")
        self.player_sprite2 = Sprite(
            "../cs3050_pokemon/sprites/" + self.enemy.get_curr_pkm().get_name().lower() + "-front.png",
            OPPONENT_SPRITE_SCALING)
        if self.state.get_state().value == State.Wait.value and self.player.get_prev_pkm() != -1:
            self.player_sprite = Sprite("../cs3050_pokemon/sprites/" + self.player.get_pokemon_list()[
                self.player.get_prev_pkm()].get_name().lower() + "-back.png")
            self.player.set_prev_pkm_index()
        if self.state.get_state().value == State.Wait.value and self.player.get_prev_pkm() != -1:
            self.player_sprite2 = Sprite("../cs3050_pokemon/sprites/" + self.enemy.get_pokemon_list()[
                self.enemy.get_prev_pkm()].get_name().lower() + "-front.png", OPPONENT_SPRITE_SCALING)
            self.enemy.set_prev_pkm_index()

        self.player_sprite.scale = 300 / (self.player_sprite.height * 1.2)
        # TODO: change these to constant variables
        self.player_sprite.center_x = 200
        # self.player_sprite.bottom = 500
        self.player_sprite.bottom = self.text_area.height + 10
        self.player_sprite2.center_x = 600
        self.player_sprite2.center_y = 725
        self.player_list.append(self.player_sprite)
        self.enemy_list.append(self.player_sprite2)
        self.background = arcade.load_texture("../cs3050_pokemon/images/fight-background.png")
        self.total_time = 0.0

    # This on_draw method renders all of the buttons and sprites depending on what the current state is
    def on_draw(self):
        """ Render the screen. """
        # print(self.player.get_curr_pkm().get_name())
        # print(self.player.chk_party())
        if (self.state.get_state().value == State.Wait.value):
            # Clear the screen
            self.clear()
            # Draw the background texture
            arcade.draw_lrwh_rectangle_textured(0, 150,
                                                SCREEN_WIDTH, SCREEN_HEIGHT,
                                                self.background)

            # Draw all the sprites.
            
            self.manager.draw()
            self.player_list.draw()
            self.enemy_list.draw()
            self.bar_sprite_list.draw()
        # if(self.state == State.PokemonSwap):
        #     self.clear()
        #     # Iterate through pokemon in party and display the sprites on screen
        #     # If you click on a sprite, it will swap and return to the battle screen
        #     # Give an option to check summary stats or click swap (called from pokemon_button onclick function)
        # if(self.state == State.Bag):
        #     self.clear()

        # When the backend determines the enemy has been defeated, change states
        if not self.enemy.chk_party():
            self.state.set_state(State.Win)
            self.state.set_rendered(False)

        if not self.player.chk_party():
            self.state.set_state(State.Loss)
            self.state.set_rendered(False)

        # if(self.state == State.Moves):
        #     self.clear()
        #     # Draw the background texture
        #     arcade.draw_lrwh_rectangle_textured(0, 150,
        #                                     SCREEN_WIDTH, SCREEN_HEIGHT,
        #                                     self.background)
        #     # Draw the sprites
        #     self.manager.draw()
        #     self.player_list.draw()
        #     self.enemy_list.draw()

        #     self.bar_sprite_list.draw()
        if (self.state.get_state().value == State.Win.value):
            self.clear()
            self.bar_sprite_list.clear()

            # TODO: Set up a winning screen for later deliverables
            arcade.set_background_color(arcade.color.RED)
            self.health_text = arcade.create_text_sprite(
                start_x=350,
                start_y=500,
                color=arcade.color.BLACK,
                text="WIN"
            )
            self.health_text.center_x = 350
            self.health_text.center_y = 500
            self.bar_sprite_list.append(self.health_text)
            self.bar_sprite_list.draw()
        if (self.state.get_state().value == State.Loss.value):
            self.clear()
            self.bar_sprite_list.clear()

            # TODO: Set up a winning screen for later deliverables
            arcade.set_background_color(arcade.color.BLUE)
            self.health_text = arcade.create_text_sprite(
                start_x=350,
                start_y=500,
                color=arcade.color.BLACK,
                text="LOSS"
            )
            self.health_text.center_x = 350
            self.health_text.center_y = 500
            self.bar_sprite_list.append(self.health_text)
            self.bar_sprite_list.draw()

        # should be handling weird swap case
        if (self.player.get_curr_pkm().get_is_fainted() and self.player.chk_party()):
            print("current player pokemon fainted - swap pokemon")
            # Render swap screen so they can switch.
            self.state.set_state(State.PokemonSwap)
            self.state.set_rendered(False)

            # TODO: Call method to render sprites to swap with
            # start_view = PokemonSwap(self.player, self.enemy)
            # start_view.setup()
            # self.window.show_view(start_view)

    # This on_update method is called each frame of the game and calls the respective update methods of the sprites
    def on_update(self, delta_time):
        """ Movement and game logic """
        # Call update to move the sprite
        self.player_list.update()
        self.enemy_list.update()
        


        # if in wait state increment total time by delta time
        if self.state.get_state().value == State.Wait.value:
            self.total_time += delta_time
            # print("waiting")

        if self.action_list[0][0] == "player" and self.action_list[0][1] == "move":
            self.enemy_health_bar.health_bar_update(self.bar_sprite_list)
            self.enemy.get_curr_pkm().set_prev_hlth(self.enemy.get_curr_pkm().get_curr_hlth())
        if self.action_list[0][0] == "enemy" and self.action_list[0][1] == "move":
            self.player_health_bar.health_bar_update(self.bar_sprite_list)
            self.player.get_curr_pkm().set_prev_hlth(self.player.get_curr_pkm().get_curr_hlth())

        self.bar_sprite_list.update()
        # if total time is greater than three seconds stop waiting and go to battle state
        if int(self.total_time) % 60 > 3:
            print("resume")
            self.total_time = 0.0
            self.action_list.pop(0)
            if len(self.action_list) == 0:
                self.state.set_state(State.Battle)
            self.state.set_rendered(False)


