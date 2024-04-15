import arcade
from arcade import load_texture
import arcade.gui
from arcade.gui import UIManager
from arcade.gui.widgets import UITextArea, UITexturePane
from battle import battle

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


# This PokemonMove class 
class PokemonMove(arcade.View):
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
        ### BUTTONS ###

        # Create two vertical BoxGroup widges to align buttons
        self.v_box = arcade.gui.UIBoxLayout()
        self.v_box_2 = arcade.gui.UIBoxLayout()

        # Create the buttons
        move_1 = arcade.gui.UIFlatButton(text=self.player.get_curr_pkm().moves[0].name, width=BUTTON_WIDTH)
        self.v_box.add(move_1.with_space_around(bottom=20))
        move_1.on_click = self.move_1_go

        move_2 = arcade.gui.UIFlatButton(text=self.player.get_curr_pkm().moves[1].name, width=BUTTON_WIDTH)
        self.v_box.add(move_2.with_space_around(bottom=20))
        move_2.on_click = self.move_2_go

        move_3 = arcade.gui.UIFlatButton(text=self.player.get_curr_pkm().moves[2].name, width=BUTTON_WIDTH)
        self.v_box_2.add(move_3.with_space_around(bottom=20))
        move_3.on_click = self.move_3_go

        move_4 = arcade.gui.UIFlatButton(text=self.player.get_curr_pkm().moves[3].name, width=BUTTON_WIDTH)
        self.v_box_2.add(move_4.with_space_around(bottom=20))
        move_4.on_click = self.move_4_go

        # Create widgets to hold the v_box and v_box_2 widgets, that will center the buttons
        self.manager.add(
            arcade.gui.UIAnchorWidget(align_x=V_BOX_X, align_y= V_BOX_Y,
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box)
        )
        self.manager.add(
            arcade.gui.UIAnchorWidget(align_x=V_BOX_2_X, align_y= V_BOX_Y,
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box_2)
        )
        
    # This setup method is called when creating all the sprites to be stored on the screen when the window is rendered
    def setup(self):
        """ Set up the game and initialize the variables. """
        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()

        # Set up the player and enemy sprites
        self.player_sprite = Sprite("../cs3050_pokemon/sprites/" + self.player.get_curr_pkm().get_name().lower() + "-back.png")
        self.player_sprite.scale = 300 / (self.player_sprite.height * 1.2)

        self.player_sprite2 = Sprite("../cs3050_pokemon/sprites/" + self.enemy.get_curr_pkm().get_name().lower() + "-front.png", OPPONENT_SPRITE_SCALING)
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
        self.clear()
        # Draw the background texture
        arcade.draw_lrwh_rectangle_textured(0, 150,
                                        SCREEN_WIDTH, SCREEN_HEIGHT,
                                        self.background)
        # Draw the sprites
        self.manager.draw()
        self.player_list.draw()
        self.enemy_list.draw()

        self.bar_sprite_list.draw()



    # This move_1_go method is called when the first move button is clicked, it passes button information
    # to the backend where the battle function is called. The results of the tern are reflected in the 
    # HealthBar Sprites
    def move_1_go(self, event):
        if(self.state.get_state().value == State.Moves.value):
            print("accessing first move")
            self.state.set_state(State.Wait)
            self.state.set_rendered(False)
            # GLOBAL_STATE = State.Battle

            btn_info = ["move", self.player.get_curr_pkm().get_moves()[0]]
            action1, action2, action_dict = battle(self.player, self.enemy, btn_info)
            self.state.set_action_list(action_dict)
            
            if(self.enemy.get_curr_pkm().get_is_fainted()):
                # Render the fight screen again with the updated sprite
                self.state.set_state(State.Wait)
                self.state.set_rendered(False)
                
            if(action1 != "win"):
                # Render the fight screen again with the updated sprite
                self.state.set_state(State.Wait)
                self.state.set_rendered(False)
                print(f"current pokemon after button press: {self.player.get_curr_pkm().get_name()}")
                self.state.set_curr_pkm(self.player.get_curr_pkm())
            else:
                self.state.add_new_action(["player", "win", "The enemy is out of pokemon"])
                self.state.set_state(State.Wait)
                self.state.set_rendered(False)

    # This move_2_go method is called when the second move button is clicked, it passes button information
    # to the backend where the battle function is called. The results of the tern are reflected in the 
    # HealthBar Sprites
    def move_2_go(self, event):
        global GLOBAL_STATE
        if(self.state.get_state().value == State.Moves.value):
            self.state.set_state(State.Wait)
            self.state.set_rendered(False)
            print("accessing second move")
            btn_info = ["move", self.player.get_curr_pkm().get_moves()[1]]
            action1, action2, action_list = battle(self.player, self.enemy, btn_info)
            self.state.set_action_list(action_list)
            if(self.enemy.get_curr_pkm().get_is_fainted()):
                # Render the fight screen again with the updated sprite
                self.state.set_state(State.Wait)
                self.state.set_rendered(False)
                self.state.set_curr_pkm(self.player.get_curr_pkm())
            if(action1 != "win"):
                # Render the fight screen again with the updated sprite
                self.state.set_state(State.Wait)
                self.state.set_rendered(False)
            else:
                self.state.add_new_action(["player", "win", "The enemy is out of pokemon"])
                self.state.set_state(State.Wait)
                self.state.set_rendered(False)
            

    # This move_3_go method is called when the third move button is clicked, it passes button information
    # to the backend where the battle function is called. The results of the tern are reflected in the 
    # HealthBar Sprites
    def move_3_go(self, event):
        if(self.state.get_state().value == State.Moves.value):
            self.state.set_state(State.Wait)
            self.state.set_rendered(False)
            print("accessing third move")
            btn_info = ["move", self.player.get_curr_pkm().get_moves()[2]]
            action1, action2, action_list = battle(self.player, self.enemy, btn_info)
            self.state.set_action_list(action_list)
            if(self.enemy.get_curr_pkm().get_is_fainted()):
                # Render the fight screen again with the updated sprite
                self.state.set_state(State.Wait)
                self.state.set_rendered(False)
                self.state.set_curr_pkm(self.player.get_curr_pkm())

            if(action1 != "win"):
                # Render the fight screen again with the updated sprite
                self.state.set_state(State.Wait)
                self.state.set_rendered(False)
            else:
                self.state.add_new_action(["player", "win", "The enemy is out of pokemon"])
                self.state.set_state(State.Wait)
                self.state.set_rendered(False)

    # This move_4_go method is called when the fourth move button is clicked, it passes button information
    # to the backend where the battle function is called. The results of the tern are reflected in the 
    # HealthBar Sprites
    def move_4_go(self, event):
        if(self.state.get_state().value == State.Moves.value):
            self.state.set_state(State.Wait)
            self.state.set_rendered(False)
            print("accessing fourth move")
            btn_info = ["move", self.player.get_curr_pkm().get_moves()[3]]
            action1, action2, action_list = battle(self.player, self.enemy, btn_info)
            self.state.set_action_list(action_list)
            if(self.enemy.get_curr_pkm().get_is_fainted()):
                # Render the fight screen again with the updated sprite
                self.state.set_state(State.Wait)
                self.state.set_rendered(False)
                self.state.set_curr_pkm(self.player.get_curr_pkm())

            if(action1 != "win"):
                # Render the fight screen again with the updated sprite
                self.state.set_state(State.Wait)
                self.state.set_rendered(False)

            else:
                self.state.add_new_action(["player", "win", "The enemy is out of pokemon"])
                self.state.set_state(State.Wait)
                self.state.set_rendered(False)


    # This on_update method is called each frame of the game and calls the respective update methods of the sprites
    def on_update(self, delta_time):
        """ Movement and game logic """
        # Call update to move the sprite
        self.player_list.update()
        self.enemy_list.update()
        self.bar_sprite_list.update()
