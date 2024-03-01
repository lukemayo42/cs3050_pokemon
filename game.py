import arcade
from arcade import load_texture
from arcade.gui import UIManager
from arcade.gui.widgets import UITextArea, UIInputText, UITexturePane
import os
from enum import Enum




class State(Enum):
    Start = 1
    World = 2
    Battle = 3

state = State.Start

SPRITE_SCALING = 3.5
MOVEMENT_SPEED = 5

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
W_SCREEN_TITLE = "Pokemon World"
B_SCREEN_TITLE = "Battle"

class Player(arcade.Sprite):

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

    def __init__(self, width, height, title):

        state = State.Battle
        # Call the parent class initializer
        super().__init__(width, height, title)

        # Background image will be stored in this variable
        self.background = None

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
        super().__init__(800, 600, "Scrollable Text", resizable=True)
        self.manager = UIManager()
        self.manager.enable()
        arcade.set_background_color(arcade.color.LIGHT_SEA_GREEN)

        bg_tex = load_texture(":resources:gui_basic_assets/window/grey_panel.png")
        text_area = UITextArea(x=0,
                               y=0,
                               width=400,
                               height=150,
                               text="TEST TEST TEST",
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


        # self.manager.add(
        #     UITexturePane(
        #         UIInputText(x=340, y=200, width=200, height=50, text="Hello"),
        #         tex=bg_tex,
        #         padding=(10, 10, 10, 10)
        #     ))
        # self.manager.add(
        #     UIInputText(x=340, y=110, width=200, height=50, text="Hello"),
        # )

        
    def setup(self):
        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.player_list = arcade.SpriteList()
        # import os
        # print("test")
        # print(os.getcwd())
        # Set up the player
        self.player_sprite = Player("../cs3050_pokemon/sprites/bulbasaur-back.png", SPRITE_SCALING)
        self.player_sprite.center_x = 200
        self.player_sprite.center_y = 235
        self.player_list.append(self.player_sprite)

        self.background = arcade.load_texture("../cs3050_pokemon/images/fight-background.png")

    def on_draw(self):
        """ Render the screen. """

        # Clear the screen
        self.clear()

        # Draw all the sprites.
        self.manager.draw()

        # Draw the background texture
        arcade.draw_lrwh_rectangle_textured(0, 150,
                                            SCREEN_WIDTH, SCREEN_HEIGHT,
                                            self.background)

        self.player_list.draw()
    
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
    window = PokemonGame(SCREEN_WIDTH, SCREEN_HEIGHT, B_SCREEN_TITLE)
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()
