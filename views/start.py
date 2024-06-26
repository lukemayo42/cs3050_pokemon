import arcade
from arcade import load_texture
import arcade.gui
from arcade.gui import UIManager
from arcade.gui.widgets import UITextArea, UITexturePane
from state import State
from views.health import Sprite

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BUTTON_WIDTH = 175

# Rules page formatting
RULES = ''' 
        Welcome to our Pokemon Game. 
        When you are ready, return to the start menu and click start to enter the world of Pokemon. You will select an avatar and then a Pokemon party of 3 Pokemon that will fight for you. Each have different attack moves and health so choose wisely. 
        When you feel ready to fight, enter the world and challenge an opponent by walking up to them. You can choose between 'Fight' which gives you 4 move options, 'Pokemon' to switch between the Pokemon in your party, and 'Items' which allows you to use special items like health potions.
        There are three unique trainers around the map with varying difficulty. You can fight each of them once (or skip them if you are feeling ready) and enter the gym (center building with the brown roof) to fight the gym trainer.
        Remember, once you enter the gym you cannot leave!'''
RULES_WIDTH = 400
RULES_HEIGHT = 350

    # This PokemonStart class is a view screen that opens up when the program is started. It gives the user
# a chance to review the rules and how to play, and then a button to start.
class PokemonStart(arcade.View):
    """
    constrctor for PokemonStart class
    """
    def __init__(self, player, enemy, state):
        super().__init__()
        self.player = player
        self.enemy = enemy
        # state.set_state(State.Start)
        self.state = state

        # Background image will be stored in this variable
        self.background = None
        arcade.set_background_color(arcade.color.WHITE)

        # Button styling
        start_style = {
            "bg_color":(50,75,125),
            "bg_color_pressed":(20, 65, 115)
        }

        # Create start button
        self.v_box = arcade.gui.UIBoxLayout()
        start_button = arcade.gui.UIFlatButton(text="Start", width=BUTTON_WIDTH * 2, style=start_style)
        # start_button = CustomButton(text="Start", width=BUTTON_WIDTH * 2, style=start_style, id=1)
        self.v_box.add(start_button.with_space_around(bottom=20))

        # Assign self.items_button as a callback to render item bag
        start_button.on_click = self.start_button_action
        self.start_button = start_button

        # Create rules button
        rules_button = arcade.gui.UIFlatButton(text="Rules", width=BUTTON_WIDTH * 2, style=start_style)
        self.v_box.add(rules_button.with_space_around(bottom=20))

        rules_button.on_click = self.rules_button_action

        self.manager = UIManager()
        self.manager.enable()
        # Create a widget to hold the v_box widget, that will center the buttons
        self.manager.add(
            arcade.gui.UIAnchorWidget(align_x=0, align_y= -SCREEN_HEIGHT / 5,
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box)
        )

    def setup(self):
        self.player_list = arcade.SpriteList()
        self.player_sprite = Sprite("../cs3050_pokemon/images/start.png")
        self.player_sprite.scale = SCREEN_HEIGHT  / (self.player_sprite.height * 3)
        self.player_sprite.center_x = SCREEN_WIDTH / 2
        self.player_sprite.center_y = 3 * SCREEN_HEIGHT / 4
        self.player_list.append(self.player_sprite)
        self.background_sky = arcade.load_texture("../cs3050_pokemon/images/screen_background.png")

    def start_button_action(self, event):
        print("starting")
        ## MAP VIEW
        if(self.state.get_state().value == State.Start.value):
            self.state.set_state(State.CharacterSelect)
            self.state.set_rendered(False)
        

    def rules_button_action(self, event):
        if(self.state.get_state().value == State.Start.value):
            print("Here is how to play the game")
            self.state.set_state(State.Rules)
            rules_view = PokemonRules(self.player, self.enemy, self.state)
            rules_view.setup()
            self.window.show_view(rules_view)

    def on_draw(self):
            # Clear the screen
            self.clear()
            # Draw the background texture
            arcade.draw_lrwh_rectangle_textured(0, 0,
                                                SCREEN_WIDTH, SCREEN_HEIGHT,
                                                self.background_sky)
            
            # Draw all the sprites.
            self.manager.draw()
            self.player_list.draw()

# This PokemonRules view class displays a scrollable textbox with the information on how to play the game.
# It has a button to return to the start screen that renders the PokemonStart view.
class PokemonRules(arcade.View):
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

        # Create "go back" button
        self.v_box = arcade.gui.UIBoxLayout()
        back_button = arcade.gui.UIFlatButton(text="Go Back", width=BUTTON_WIDTH * 2, style=button_style)
        self.v_box.add(back_button.with_space_around(bottom=20))

        # Assign self.items_button as a callback to render item bag
        back_button.on_click = self.back_button_action

        self.manager = UIManager()
        self.manager.enable()
        # Create a widget to hold the v_box widget, that will center the buttons
        self.manager.add(
            arcade.gui.UIAnchorWidget(align_x=0, align_y= -SCREEN_HEIGHT / 3,
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box)
        )
        # Rules text scrollable textbox
        bg_tex = load_texture(":resources:gui_basic_assets/window/grey_panel.png")
        rules_area = UITextArea(x= SCREEN_WIDTH / 4,
                               y=SCREEN_HEIGHT / 3,
                               width=RULES_WIDTH,
                               height=RULES_HEIGHT,
                               text=RULES,
                               text_color=(0, 0, 0, 255))
        self.manager.add(
            UITexturePane(
                rules_area.with_space_around(right=20),
                tex=bg_tex,
                padding=(10, 10, 10, 10)
            )
        )

    def setup(self):
        self.background_sky = arcade.load_texture("../cs3050_pokemon/images/screen_background.png")
        print("setting up rules")

    def back_button_action(self, event):
        if(self.state.get_state().value == State.Rules.value):
            print("returning to start screen")
            self.state.set_state(State.Start)
            start_view = PokemonStart(self.player, self.enemy, self.state)
            start_view.setup()
            self.window.show_view(start_view)


    def on_draw(self):
        # Clear the screen
        self.clear()
        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            SCREEN_WIDTH, SCREEN_HEIGHT,
                                            self.background_sky)
        # Draw all the sprites.
        self.manager.draw()
