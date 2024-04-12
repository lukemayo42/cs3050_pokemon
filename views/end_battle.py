import arcade
from arcade import load_texture
import arcade.gui
from arcade.gui import UIManager
from arcade.gui.widgets import UITextArea, UITexturePane
from state import State

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BUTTON_WIDTH = 175


class EndBattle(arcade.View):
    def __init__(self, player, enemy, state):
        super().__init__()
        self.player = player
        self.enemy = enemy
        self.state = state

        # Background image will be stored in this variable
        self.background = None
        arcade.set_background_color(arcade.color.WHITE)

        # Button styling
        button_style = {
            "bg_color":(50,75,125),
            "bg_color_pressed":(20, 65, 115)
        }

        # Create "play back" button
        self.v_box = arcade.gui.UIBoxLayout()
        play_again_button = arcade.gui.UIFlatButton(text="Play Again", width=BUTTON_WIDTH * 2, style=button_style)
        self.v_box.add(play_again_button.with_space_around(bottom=20))

        # on button click return to main start screen
        play_again_button.on_click = self.play_again_button_action

        self.manager = UIManager()
        self.manager.enable()
        # Create a widget to hold the v_box widget, that will center the buttons
        self.manager.add(
            arcade.gui.UIAnchorWidget(align_x=0, align_y= -SCREEN_HEIGHT / 3,
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box)
        )
        display_text = ""
        
        #determine text to be displayed based on state
        if self.state.get_state().value == State.Win.value:
            display_text ="You Win!"
        else:
            display_text = "You Lose!"
    
        self.text = arcade.create_text_sprite (
            start_x=SCREEN_WIDTH / 2 - 100,
            start_y=SCREEN_HEIGHT / 2,
            color=arcade.color.BLACK,
            text = display_text,
            font_size = 40
        )

        

    def setup(self):
        self.text_list = arcade.SpriteList()
        self.text_list.append(self.text)
        self.background_sky = arcade.load_texture("../cs3050_pokemon/images/screen_background.png")


    def play_again_button_action(self, event):
        #return to start screen and heal all pokemon
        
        if(self.state.get_state().value == State.Loss.value or self.state.get_state().value == State.Win.value):
            print("returning to start screen")
            self.state.set_state(State.Start)
            print("Button pressed")
            self.state.set_rendered(False)



    def on_draw(self):
        # Clear the screen
        self.clear()

        #draw background
        arcade.draw_lrwh_rectangle_textured(0, 0,
                                    SCREEN_WIDTH, SCREEN_HEIGHT,
                                    self.background_sky)
    
        # Draw all the sprites.
        self.manager.draw()
        self.text_list.draw()