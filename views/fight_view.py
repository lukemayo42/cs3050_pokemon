import arcade
from arcade import load_texture
import arcade.gui
from arcade.gui import UIManager
from arcade.gui.widgets import UITextArea, UITexturePane

from views.health import HealthBar
from views.health import Sprite
from state import State
from state import BattleState

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
class PokemonGame(arcade.View):
    """
    constructor for PokemonGame class
    attributes of class
    width - width of the screen in pixels - int
    height - heigth of the screen in pixels - int
    title - the name of the screen - string
    player - Character object representing the player - Character
    enemy - Character object representing the enemy trainer - Character
    """

    def __init__(self, player, enemy, state):
        super().__init__()
        # Start in the battle state for deliverable 1
        self.state = state
        self.player = player
        self.enemy = enemy

        # Background image will be stored in this variable
        self.background = None

        # Health bar
        self.bar_sprite_list = arcade.SpriteList()
        self.enemy_health_bar = HealthBar(self.enemy.get_curr_pkm(), self.bar_sprite_list, 350, 500, 515, True, self.enemy.get_curr_pkm().get_curr_hlth())
        self.player_health_bar = HealthBar(self.player.get_curr_pkm(), self.bar_sprite_list, 550, 250, 265, True, self.player.get_curr_pkm().get_curr_hlth())

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
                                    width=SCREEN_WIDTH / 2,
                                    height=SCREEN_HEIGHT / 4,
                                    text="What will " + self.player.get_curr_pkm().get_name() + " do?",
                                    font_size=FONT_SIZE,
                                    text_color=arcade.color.BLACK)
        self.manager.add(
            UITexturePane(
                self.text_area.with_space_around(right=20),
                tex=bg_tex,
                padding=(10, 10, 10, 10)
            )
        )
        bg_tex = load_texture(":resources:gui_basic_assets/window/grey_panel.png")
        move_text_area = UITextArea(x=400,
                                    y=0,
                                    width=SCREEN_WIDTH / 2,
                                    height=SCREEN_HEIGHT / 4,
                                    font_size=50,
                                    text_color=(0, 0, 0, 255))
        self.manager.add(
            UITexturePane(
                move_text_area.with_space_around(right=20),
                tex=bg_tex,
                padding=(10, 10, 10, 10)
            )
        )

        ###### BUTTONS #########
        # Create a vertical BoxGroup to align buttons
        self.v_box = arcade.gui.UIBoxLayout()
        self.v_box_2 = arcade.gui.UIBoxLayout()

        # Create the fight button
        fight = arcade.gui.UIFlatButton(text="Fight", width=BUTTON_WIDTH)
        self.v_box.add(fight.with_space_around(bottom=20))

        # Assign self.fight_action as callback
        fight.on_click = self.fight_action

        # Create the pokemon button
        pokemon_button = arcade.gui.UIFlatButton(text="Pokemon", width=BUTTON_WIDTH)
        self.v_box.add(pokemon_button.with_space_around(bottom=20))

        # Assign self.pokemon_button_action as a callback to render pokemon party
        pokemon_button.on_click = self.pokemon_button_action

        # Create the item bag button
        items_button = arcade.gui.UIFlatButton(text="Items", width=BUTTON_WIDTH)
        self.v_box_2.add(items_button.with_space_around(bottom=20))

        # Assign self.items_button as a callback to render item bag
        items_button.on_click = self.items_button_action

        # Create a widget to hold the v_box widget, that will center the buttons
        self.manager.add(
            arcade.gui.UIAnchorWidget(align_x=V_BOX_X, align_y=V_BOX_Y,
                                      anchor_x="center_x",
                                      anchor_y="center_y",
                                      child=self.v_box)
        )

        # Create a widget to hold the v_box_2 widget, that will center the buttons
        self.manager.add(
            arcade.gui.UIAnchorWidget(align_x=V_BOX_2_X, align_y=V_BOX_2_Y,
                                      anchor_x="center_x",
                                      anchor_y="center_y",
                                      child=self.v_box_2)
        )

    # This fight_action method is called when the fight button is clicked, it changes the state and adds new buttons
    def fight_action(self, event):
        if (self.state.get_state().value == State.Battle.value):
            self.state.set_state(State.Moves)
            self.state.set_rendered(False)

    def pokemon_button_action(self, event):
        if (self.state.get_state().value == State.Battle.value):
            self.state.set_state(State.PokemonSwap)
            self.state.set_rendered(False)
            
    def items_button_action(self, event):
        if (self.state.get_state().value == State.Battle.value):
            self.state.set_state(State.Item)
            self.state.set_rendered(False)

            
    # This setup method is called when creating all the sprites to be stored on the screen when the window is rendered
    def setup(self):
        """ Set up the game and initialize the variables. """
        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()

        # Set up the player and enemy sprites
        self.player_sprite = Sprite(
            "../cs3050_pokemon/sprites/" + self.player.get_curr_pkm().get_name().lower() + "-back.png")
        self.player_sprite.scale = 300 / (self.player_sprite.height * 1.2)

        self.player_sprite2 = Sprite(
            "../cs3050_pokemon/sprites/" + self.enemy.get_curr_pkm().get_name().lower() + "-front.png",
            OPPONENT_SPRITE_SCALING)
        # TODO: change these to constant variables
        self.player_sprite.center_x = 200
        # self.player_sprite.bottom = 500
        self.player_sprite.bottom = self.text_area.height + 10
        self.player_sprite2.center_x = 600
        self.player_sprite2.center_y = 725
        self.player_list.append(self.player_sprite)
        self.enemy_list.append(self.player_sprite2)
        self.background = arcade.load_texture("../cs3050_pokemon/images/fight-background.png")

    # This on_draw method renders all of the buttons and sprites depending on what the current state is
    def on_draw(self):
        """ Render the screen. """
        if (self.state.get_state().value == State.Battle.value):

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

        # When the backend determines the enemy has been defeated, change states
        if not self.enemy.chk_party() and self.state.get_battle_state().value == BattleState.GymLeader.value:
            self.state.add_new_action(["player", "fullwin", "The enemy is out of pokemon"])
            self.state.set_state(State.Wait)
            self.state.set_rendered(False)
        if not self.enemy.chk_party() and self.state.get_battle_state().value != BattleState.GymLeader.value:
            self.state.add_new_action(["player", "win", "The enemy is out of pokemon"])
            self.state.set_state(State.Wait)
            self.state.set_rendered(False)

        if not self.player.chk_party():
            self.state.add_new_action(["player", "lost", "You are out of pokemon"])
            self.state.set_state(State.Wait)
            self.state.set_rendered(False)

        if (self.state.get_state().value == State.Win.value):
            self.clear()
            self.bar_sprite_list.clear()

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

        
    # This on_update method is called each frame of the game and calls the respective update methods of the sprites
    def on_update(self, delta_time):
        """ Movement and game logic """
        # Call update to move the sprite
        self.player_list.update()
        self.enemy_list.update()
        self.bar_sprite_list.update()

