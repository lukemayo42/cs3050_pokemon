import arcade
from arcade import load_texture
import arcade.gui
from arcade.gui import UIManager
from arcade.gui.widgets import UITextArea, UIInputText, UITexturePane
import os
from enum import Enum
from battle import battle
import Character
from pokemon import pokemon
from move import move



class State(Enum):
    Start = 1
    World = 2
    Battle = 3
    Moves = 4

state = State.Battle

SPRITE_SCALING = 3.5
OPPONENT_SPRITE_SCALING = 3
MOVEMENT_SPEED = 5

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
W_SCREEN_TITLE = "Pokemon World"
B_SCREEN_TITLE = "Battle"


# Create subclass for the user
# Subclass for pokemon
# Subclass for enemy
class Sprite(arcade.Sprite):

    def update(self):
        """ Move the player """
        # Move player.
        # Remove these lines if physics engine is moving player.
        self.center_x += self.change_x
        self.center_y += self.change_y

        # Check for out-of-bounds
        if self.left < 0:
            self.left = 0
        elif self.right > SCREEN_WIDTH - 1:
            self.right = SCREEN_WIDTH - 1

        if self.bottom < 0:
            self.bottom = 0
        elif self.top > SCREEN_HEIGHT - 1:
            self.top = SCREEN_HEIGHT - 1

class PokemonGame(arcade.Window):

    def __init__(self, width, height, title, player, enemy):

        state = State.Battle
        # Call the parent class initializer
        super().__init__(width, height, title)
        self.player = player
        self.enemy = enemy
        # Background image will be stored in this variable
        self.background = None

        self.background2 = None

        # Variables that will hold sprite lists
        self.player_list = None

        # Set up the player info
        self.player_sprite = None

        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        # Set the background color

        
        
        ############ TEXT BOX EXAMPLE
        self.manager = UIManager()
        self.manager.enable()
        # arcade.set_background_color(arcade.color.LIGHT_SEA_GREEN)

        bg_tex = load_texture(":resources:gui_basic_assets/window/grey_panel.png")
        text_area = UITextArea(x=0,
                               y=0,
                               width=400,
                               height=150,
                               text="What will Bulbasaur do?",
                               font_size=20,
                               text_color=(0, 0, 0, 255))
        self.manager.add(
            UITexturePane(
                text_area.with_space_around(right=20),
                tex=bg_tex,
                padding=(10, 10, 10, 10)
            )
        )

        bg_tex = load_texture(":resources:gui_basic_assets/window/grey_panel.png")
        move_text_area = UITextArea(x=400,
                               y=0,
                               width=400,
                               height=150,
                               text="FIGHT BAG\nPOKeMON RUN",
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

        # Create the buttons
        fight = arcade.gui.UIFlatButton(text="Fight", width=200)
        self.v_box.add(fight.with_space_around(bottom=20))

       

        # assign self.on_click_start as callback
        fight.on_click = self.fight_action

        # Create a widget to hold the v_box widget, that will center the buttons
        self.manager.add(
            arcade.gui.UIAnchorWidget(align_x=100, align_y= -200,
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box)
        )
        # self.manager.add(
        #     UITexturePane(
        #         UIInputText(x=340, y=200, width=200, height=50, text="Hello"),
        #         tex=bg_tex,
        #         padding=(10, 10, 10, 10)
        #     ))
        # self.manager.add(
        #     UIInputText(x=340, y=110, width=200, height=50, text="Hello"),
        # )

    def fight_action(self, event):
        state = State.Moves
        self.add_move_buttons()
        self.on_draw()

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.player_list = arcade.SpriteList()
        # import os
        # print("test")
        # print(os.getcwd())
        # Set up the player
        self.player_sprite = Sprite("../cs3050_pokemon/sprites/bulbasaur-back.png", SPRITE_SCALING)
        self.player_sprite2 = Sprite("../cs3050_pokemon/sprites/charizard-front.png", OPPONENT_SPRITE_SCALING)
        self.player_sprite.center_x = 200
        self.player_sprite.center_y = 235
        self.player_sprite2.center_x = 600
        self.player_sprite2.center_y = 725
        self.player_list.append(self.player_sprite)
        self.player_list.append(self.player_sprite2)

        self.background = arcade.load_texture("../cs3050_pokemon/images/fight-background.png")

    def on_draw(self):
        """ Render the screen. """
        if(state == State.Battle):
            # Clear the screen
            self.clear()
            # Draw the background texture
            arcade.draw_lrwh_rectangle_textured(0, 150,
                                                SCREEN_WIDTH, SCREEN_HEIGHT,
                                                self.background)
            # Draw all the sprites.
            self.manager.draw()
            self.player_list.draw()
        if(state == State.Moves):
            self.clear()
            # Draw the background texture
            arcade.draw_lrwh_rectangle_textured(0, 150,
                                            SCREEN_WIDTH, SCREEN_HEIGHT,
                                            self.background2)
            self.manager.draw()
            self.player_list.draw()

    
    def add_move_buttons(self):
        self.v_box.clear()
        # Create a vertical BoxGroup to align buttons
        self.v_box = arcade.gui.UIBoxLayout()
        self.v_box_2 = arcade.gui.UIBoxLayout()

        # Create the buttons
        move_1 = arcade.gui.UIFlatButton(text="Move 1", width=175)
        self.v_box.add(move_1.with_space_around(bottom=20))

        # assign self.on_click_start as callback
        move_1.on_click = self.move_1_go

        move_2 = arcade.gui.UIFlatButton(text="Move 2", width=175)
        self.v_box.add(move_2.with_space_around(bottom=20))

        # assign self.on_click_start as callback
        move_2.on_click = self.move_2_go

        move_3 = arcade.gui.UIFlatButton(text="Move 3", width=175)
        self.v_box_2.add(move_3.with_space_around(bottom=20))

        # assign self.on_click_start as callback
        move_3.on_click = self.move_3_go

        move_4 = arcade.gui.UIFlatButton(text="Move 4", width=175)
        self.v_box_2.add(move_4.with_space_around(bottom=20))

        # assign self.on_click_start as callback
        move_4.on_click = self.move_4_go

        # Create a widget to hold the v_box widget, that will center the buttons
        self.manager.add(
            arcade.gui.UIAnchorWidget(align_x=100, align_y= -200,
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box)
        )
        # Create a widget to hold the v_box_2 widget, that will center the buttons
        self.manager.add(
            arcade.gui.UIAnchorWidget(align_x=300, align_y= -200,
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box_2)
        )



    def move_1_go(self, event):
        print("accessing first move")
        self.update_background()
        btn_info = ["move", self.player.get_curr_pkm().get_moves()[0]]
        battle(self.player, self.enemy, btn_info)

    def move_2_go(self, event):
        print("accessing second move")
        self.update_background()
        btn_info = ["move", self.player.get_curr_pkm().get_moves()[1]]
        battle(self.player, self.enemy, btn_info)

    def move_3_go(self, event):
        print("accessing third move")
        self.update_background()
        btn_info = ["move", self.player.get_curr_pkm().get_moves()[2]]
        battle(self.player, self.enemy, btn_info)

    def move_4_go(self, event):
        print("accessing fourth move")
        self.update_background()
        btn_info = ["move", self.player.get_curr_pkm().get_moves()[3]]
        battle(self.player, self.enemy, btn_info)

    def update_player_speed(self):

        # Calculate speed based on the keys pressed
        self.player_sprite.change_x = 0
        self.player_sprite.change_y = 0

        if self.up_pressed and not self.down_pressed:
            self.player_sprite.change_y = MOVEMENT_SPEED
        elif self.down_pressed and not self.up_pressed:
            self.player_sprite.change_y = -MOVEMENT_SPEED
        if self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = MOVEMENT_SPEED
    
    def update_background(self):
        self.background2 = arcade.load_texture("../cs3050_pokemon/images/green.png")
        # Draw the background texture
        arcade.draw_lrwh_rectangle_textured(0, 150,
                                            SCREEN_WIDTH, SCREEN_HEIGHT,
                                            self.background2)

    def on_update(self, delta_time):
        """ Movement and game logic """

        # Call update to move the sprite
        self.player_list.update()

    def on_key_press(self, key, modifiers):
        """Listen for a key press from user """

        if(state == State.World):
            if key == arcade.key.UP:
                self.up_pressed = True
                self.update_player_speed()
            elif key == arcade.key.DOWN:
                self.down_pressed = True
                self.update_player_speed()
            elif key == arcade.key.LEFT:
                self.left_pressed = True
                self.update_player_speed()
            elif key == arcade.key.RIGHT:
                self.right_pressed = True
                self.update_player_speed()

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if(state == State.World):
            if key == arcade.key.UP:
                self.up_pressed = False
                self.update_player_speed()
            elif key == arcade.key.DOWN:
                self.down_pressed = False
                self.update_player_speed()
            elif key == arcade.key.LEFT:
                self.left_pressed = False
                self.update_player_speed()
            elif key == arcade.key.RIGHT:
                self.right_pressed = False
                self.update_player_speed()



def main():
    """ Main function """
    
    

    window = PokemonGame(SCREEN_WIDTH, SCREEN_HEIGHT, B_SCREEN_TITLE, trainer1, trainer2)
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()
