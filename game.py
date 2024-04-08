### NO LONGER USED (game runs through main.py)

import arcade
from arcade import load_texture
import arcade.gui
from arcade.gui import UIManager
from arcade.gui.widgets import UITextArea, UIInputText, UITexturePane
import os
from enum import Enum
from battle import battle
from Character import Character
from pokemon import pokemon
from move import move
import pokemon_objects
import item_objects
import math
import time

# Enum to hold the current state of the game, used to update the screen rendering
class State(Enum):
    Start = 1
    World = 2
    Battle = 3
    Moves = 4
    Win = 5
    PokemonSwap = 6
    Bag = 7
    Loss = 8
    Swap = 9
    Item = 10
    Stat = 11
    Rules = 12

# Constants for sprite rendering and sprite movement
SPRITE_SCALING = 3.5
OPPONENT_SPRITE_SCALING = 3
MOVEMENT_SPEED = 5
ANIMATION_SPEED = 15

# Constants for health bar sprites
HEALTH_BAR_SCALAR = 125
HEALTH_BAR_BORDER = 12

# Constants for window attributes
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
W_SCREEN_TITLE = "Pokemon World"
B_SCREEN_TITLE = "Battle"
FONT_SIZE = 20

# Button formatting
BUTTON_WIDTH = 175
V_BOX_X = 100
V_BOX_Y = -225
V_BOX_2_X = 300
V_BOX_2_Y = -190

# Rules page formatting
RULES = ''' **IMPORTANT** In order to fight, press the right arrow key in the map until the battle pops up!
        Welcome to our Pokemon Game. 
        When you are ready, return to the start menu and click start to enter the world of Pokemon. You will select a Pokemon party of 3 Pokemon that will fight for you. Each have different attack moves and health so choose wisely. 
        When you feel ready to fight, enter the gym and challenge an opponent. You can choose between 'Fight' which gives you 4 move options, 'Pokemon' to switch between the Pokemon in your party, and 'Items' which allows you to use special items like health potions.'''
RULES_WIDTH = 400
RULES_HEIGHT = 350

GLOBAL_STATE = State.Start

# Possible TODOs
# Create subclass for the user
# Subclass for pokemon
# Subclass for enemy
#TODO: fix buttons so that you cant press them on the wrong screen

# This HealthBar class is a subclass of the Sprite arcade class that displays the health and name
# of pokemon on the screen in text sprites. It has a health_bar_update method that rewrites the sprite.
class HealthBar(arcade.Sprite):
    def __init__(self, pokemon, sprite_list, pos_x, pos_y, name_pos):
        super().__init__()
        self.pokemon = pokemon
        self.health = pokemon.get_curr_hlth()
        self.max_health = pokemon.get_max_hlth()
        self.name = pokemon.get_name()
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.name_pos = name_pos
        background_color = arcade.color.BLACK
        foreground_color = arcade.color.ASH_GREY

        # Create the boxes needed to represent the indicator bar
        self.background_box = arcade.SpriteSolidColor(
            HEALTH_BAR_SCALAR * 2,
            HEALTH_BAR_SCALAR + 2 * HEALTH_BAR_BORDER,
            background_color
        )
        self.background_box.center_x = pos_x
        self.background_box.center_y = pos_y
        sprite_list.append(self.background_box)
        self.foreground_box = arcade.SpriteSolidColor(
            HEALTH_BAR_SCALAR * 2 - 2 * HEALTH_BAR_BORDER,
            HEALTH_BAR_SCALAR,
            foreground_color
        )
        self.foreground_box.center_x = pos_x
        self.foreground_box.center_y = pos_y
        sprite_list.append(self.foreground_box)
        self.health_text = arcade.create_text_sprite (
            start_x=pos_x,
            start_y=pos_y,
            color=background_color,
            text = str(math.trunc(self.health)) + " / " + str(self.max_health)
        )
        self.health_text.center_x = pos_x
        self.health_text.center_y = pos_y
        sprite_list.append(self.health_text)
        self.name_text = arcade.create_text_sprite(
            start_x=pos_x,
            start_y=name_pos,
            color=background_color,
            text=str(self.pokemon.get_name())
        )
        self.name_text.center_x = pos_x
        self.name_text.center_y = name_pos
        sprite_list.append(self.name_text)

    # This health_bar_update method replaces the previous text box displaying health with the updated health
    def health_bar_update(self, sprite_list):
        self.health = self.pokemon.get_curr_hlth()
        self.health_text.kill()
        if(math.trunc(self.health) == 0 and self.health > 0):
            self.health_text = arcade.create_text_sprite (
                start_x=self.pos_x,
                start_y=self.pos_y,
                color=arcade.color.BLACK,
                text = str(math.trunc(self.health) + 1) + " / " + str(self.max_health)
            )
        else:
            self.health_text = arcade.create_text_sprite (
                start_x=self.pos_x,
                start_y=self.pos_y,
                color=arcade.color.BLACK,
                text = str(math.trunc(self.health)) + " / " + str(self.max_health)
            )
        self.health_text.center_x = self.pos_x
        self.health_text.center_y = self.pos_y
        sprite_list.append(self.health_text)

# This Sprite subclass is similar to the parent class but it will be used to store movement logic
# for later deliverables.
class Sprite(arcade.Sprite):
    def update(self):
        """ Move the player """
        # Move player.
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
# This PokemonStart class is a view screen that opens up when the program is started. It gives the user
# a chance to review the rules and how to play, and then a button to start.
class PokemonStart(arcade.View):
    """
    constrctor for PokemonStart class
    """
    def __init__(self, player, enemy):
        super().__init__()
        self.player = player
        self.enemy = enemy
        self.state = State.Start

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
        self.v_box.add(start_button.with_space_around(bottom=20))

        # Assign self.items_button as a callback to render item bag
        start_button.on_click = self.start_button_action

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
        self.background = arcade.load_texture("../cs3050_pokemon/images/start.png")

    def start_button_action(self, event):
        #TODO: switch screen to choosing pokemon party
        print("starting")
        # fight_view = PokemonGame(self.player, self.enemy)
        # fight_view.setup()
        # self.window.show_view(fight_view)

        ## MAP VIEW
        global GLOBAL_STATE
        if(GLOBAL_STATE == State.Start):
            GLOBAL_STATE = State.World
            map_view = WorldMap(self.player, self.enemy)
            map_view.setup()
            self.window.show_view(map_view)

    def rules_button_action(self, event):
        # TODO: Render a list of rules/how to play
        global GLOBAL_STATE
        if(GLOBAL_STATE == State.Start):
            print("Here is how to play the game")
            GLOBAL_STATE = State.Rules
            rules_view = PokemonRules(self.player, self.enemy)
            rules_view.setup()
            self.window.show_view(rules_view)

    def on_draw(self):
            # Clear the screen
            self.clear()
            # Draw the background texture
            arcade.draw_lrwh_rectangle_textured(0, 150,
                                                SCREEN_WIDTH, SCREEN_HEIGHT,
                                                self.background)
            # Draw all the sprites.
            self.manager.draw()

MAP_CHARACTER_SCALING = 0.5


# How fast to move, and how fast to run the animation

MAP_MOVEMENT_SPEED = 1.5

MAP_UPDATES_PER_FRAME = 5



# Constants used to track if the player is facing left or right

MAP_RIGHT_FACING = 0

MAP_LEFT_FACING = 1




def load_texture_pair(filename):

    """

    Load a texture pair, with the second being a mirror image.

    """

    return [

        arcade.load_texture(filename),

        arcade.load_texture(filename, flipped_horizontally=True)

    ]


class PlayerCharacter(arcade.Sprite):
    def __init__(self):

        # Set up parent class
        super().__init__()


        # Default to face-right

        self.character_face_direction = MAP_RIGHT_FACING

        # Used for flipping between image sequences

        self.cur_texture = 0

        self.scale = MAP_CHARACTER_SCALING

        # Adjust the collision box. Default includes too much empty space

        # side-to-side. Box is centered at sprite center, (0, 0)

        self.points = [[-22, -64], [22, -64], [22, 28], [-22, 28]]

        # --- Load Textures ---

        # Images from Kenney.nl's Asset Pack 3

        # main_path = ":resources:images/animated_characters/female_adventurer/femaleAdventurer"

        # main_path = ":resources:images/animated_characters/female_person/femalePerson"

        main_path = ":resources:images/animated_characters/male_person/malePerson"

        # main_path = ":resources:images/animated_characters/male_adventurer/maleAdventurer"

        # main_path = ":resources:images/animated_characters/zombie/zombie"

        # main_path = ":resources:images/animated_characters/robot/robot"



        # Load textures for idle standing

        self.idle_texture_pair = load_texture_pair(f"{main_path}_idle.png")


        # Load textures for walking

        self.walk_textures = []

        for i in range(8):

            texture = load_texture_pair(f"{main_path}_walk{i}.png")

            self.walk_textures.append(texture)

    def update_animation(self, delta_time: float = 1 / 60):

        # Figure out if we need to flip face left or right

        if self.change_x < 0 and self.character_face_direction == MAP_RIGHT_FACING:

            self.character_face_direction = MAP_LEFT_FACING

        elif self.change_x > 0 and self.character_face_direction == MAP_LEFT_FACING:

            self.character_face_direction = MAP_RIGHT_FACING



        # Idle animation

        if self.change_x == 0 and self.change_y == 0:

            self.texture = self.idle_texture_pair[self.character_face_direction]

            return



        # Walking animation

        self.cur_texture += 1

        if self.cur_texture > 7 * MAP_UPDATES_PER_FRAME:

            self.cur_texture = 0

        frame = self.cur_texture // MAP_UPDATES_PER_FRAME

        direction = self.character_face_direction

        self.texture = self.walk_textures[frame][direction]


class WorldMap(arcade.View):
    """ Main application class. """

    # def __init__(self, width, height, title):
    def __init__(self, player, enemy):
        """ Set up the game and initialize the variables. """
        # super().__init__(width, height, title)
        super().__init__()
        self.pkm_player = player
        self.pkm_enemy = enemy

        # Sprite lists
        self.physics_engine = None
        self.player_list = None

        # Set up bounds on map
        self.wall_list = None

        # Set up the player
        self.player = None

        # Set up map image as background
        self.background = None

    def setup(self):
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        # Set up the player
        self.player = PlayerCharacter()

        self.player.center_x = 50
        self.player.center_y = 450
        self.player.scale = 0.4

        self.player_list.append(self.player)

        # -- Set up the walls
        # Create a row of boxes
        for x in range(0, 650, 64):
            wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png",
                                 MAP_CHARACTER_SCALING)
            wall.center_x = x
            wall.center_y = 0
            self.wall_list.append(wall)

        # Create a row of boxes
        for x in range(400, 600, 64):
            wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png",
                                 MAP_CHARACTER_SCALING)
            wall.center_x = x
            wall.center_y = 580
            self.wall_list.append(wall)

        # Create a row of boxes
        for x in range(80, 350, 64):
            wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png",
                                 MAP_CHARACTER_SCALING)
            wall.center_x = x
            wall.center_y = 520
            self.wall_list.append(wall)

        # Create a row of boxes
        for x in range(500, 580, 24):
            wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png",
                                 MAP_CHARACTER_SCALING-0.3)
            wall.center_x = x
            wall.center_y = 240
            self.wall_list.append(wall)

        # Create a row of boxes
        for x in range(330, 520, 64):
            wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png",
                                 MAP_CHARACTER_SCALING + 0.2)
            wall.center_x = x
            wall.center_y = 120
            self.wall_list.append(wall)

        wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png",
                             MAP_CHARACTER_SCALING + 0.7)
        wall.center_x = 220
        wall.center_y = 340
        self.wall_list.append(wall)

        wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png",
                             MAP_CHARACTER_SCALING + 0.2)
        wall.center_x = 460
        wall.center_y = 430
        self.wall_list.append(wall)

        wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png",
                             MAP_CHARACTER_SCALING + 0.2)
        wall.center_x = 420
        wall.center_y = 280
        self.wall_list.append(wall)

        wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png",
                             MAP_CHARACTER_SCALING - 0.2)
        wall.center_x = 305
        wall.center_y = 185
        self.wall_list.append(wall)

        # Create a column of boxes
        for y in range(250, 380, 34):
            wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png",
                                 MAP_CHARACTER_SCALING - 0.2)
            wall.center_x = 490
            wall.center_y = y
            self.wall_list.append(wall)

        # Create a column of boxes
        for y in range(310, 430, 64):
            wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png",
                                 MAP_CHARACTER_SCALING+0.2)
            wall.center_x = 310
            wall.center_y = y
            self.wall_list.append(wall)

        # Create a column of boxes
        for y in range(0, 700, 64):
            wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png",
                                 MAP_CHARACTER_SCALING)
            wall.center_x = 50
            wall.center_y = y
            self.wall_list.append(wall)

        # Create a column of boxes
        for y in range(0, 700, 64):
            wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png",
                                 MAP_CHARACTER_SCALING)
            wall.center_x = 600
            wall.center_y = y
            self.wall_list.append(wall)

        # Create a column of boxes
        for y in range(120, 220, 54):
            wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png",
                                 MAP_CHARACTER_SCALING+0.1)
            wall.center_x = 185
            wall.center_y = y
            self.wall_list.append(wall)

        self.physics_engine = arcade.PhysicsEngineSimple(self.player, self.wall_list)

        # Set the background color

        arcade.set_background_color(arcade.color.AMAZON)
        self.background = arcade.load_texture("images/world_background.png")

    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        self.clear()

        # Draw all the sprites.

        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        #self.wall_list.draw()
        self.player_list.draw()

    def on_key_press(self, key, modifiers):
        """
        Called whenever a key is pressed.
        """
        if key == arcade.key.UP:
            self.player.change_y = MAP_MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            self.player.change_y = -MAP_MOVEMENT_SPEED
        elif key == arcade.key.LEFT:
            self.player.change_x = -MAP_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player.change_x = MAP_MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """
        Called when the user releases a key.
        """
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player.change_x = 0

    def on_update(self, delta_time):
        """ Movement and game logic """

        # Move the player
        self.player_list.update()

        # Update the players animation

        self.player_list.update_animation()
        self.physics_engine.update()

        # TEMPORARY SOLUTION TO START FIGHT
        global GLOBAL_STATE
        if(self.player.center_x >= 130 and self.player.center_x <= 140 and GLOBAL_STATE == State.World):
            GLOBAL_STATE = State.Battle
            fight_view = PokemonGame(self.pkm_player, self.pkm_enemy)
            fight_view.setup()
            self.window.show_view(fight_view)

# This PokemonSwap view class gives the fighter a chance to switch between all of the pokemon in their party during the fight.
class PokemonSwap(arcade.View):
    def __init__(self, player, enemy):
        super().__init__()
        self.player = player
        self.enemy = enemy
        self.pokemon = player.get_curr_pkm()
        self.state = State.Swap

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
                sprite.center_y = i * SCREEN_WIDTH / 3.2
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
                if(self.pokemon_list[i].get_is_fainted()):
                    self.create_pokemon_buttons(SCREEN_HEIGHT, sprite.bottom - SCREEN_HEIGHT/ 30, i == 1, True)
                else:   
                    self.create_pokemon_buttons(SCREEN_HEIGHT, sprite.bottom - SCREEN_HEIGHT/ 30, i == 1, False)
        print("here is your pokemon party")

    def back_button_action(self, event):
        # switch screen to fighting screen
        global GLOBAL_STATE
        if(GLOBAL_STATE == State.Swap):
            print("returning to fight screen")
            GLOBAL_STATE = State.Battle
            fight_view = PokemonGame(self.player, self.enemy)
            fight_view.setup()
            self.window.show_view(fight_view)

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
            self.manager.add(
                arcade.gui.UIAnchorWidget(align_x=pos_x / 3, align_y=V_BOX_Y,
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
                arcade.gui.UIAnchorWidget(align_x=pos_x / 3, align_y= SCREEN_HEIGHT / 9,
                    anchor_x="center_x",
                    anchor_y="center_y",
                    child=self.button_box_2)
            )
    def generate_stats_view_1(self, event):
        self.index = 1
        self.generate_stats()

    def swap_action_1(self, event):
        self.index = 1
        self.swap_pokemon()

    def generate_stats_view_2(self, event):
        self.index = 2
        self.generate_stats()

    def swap_action_2(self, event):
        self.index = 2
        self.swap_pokemon()

    def generate_stats(self):
        # Get the selected pokemon and pass it to the stats view
        pokemon = self.player.get_pokemon_list()[self.index]
        global GLOBAL_STATE
        if(GLOBAL_STATE == State.Swap):
            print("going to stats screen")
            GLOBAL_STATE = State.Stat
            stats_view = PokemonStats(self.player, self.enemy, pokemon)
            stats_view.setup()
            self.window.show_view(stats_view)

    def swap_pokemon(self):
        # Call backend method to swap the pokemon order so that the first pokemon is back in front
        # Return to the battle screen
        global GLOBAL_STATE
        if(not self.player.get_curr_pkm().get_is_fainted()):
            btn_info = ["swap", self.index]
            player_action, enemy_action = battle(self.player, self.enemy, btn_info)
            if(player_action != "fainted" and GLOBAL_STATE == State.Swap):
                GLOBAL_STATE = State.Battle
                print("returning to battle screen")
                fight_view = PokemonGame(self.player, self.enemy)
                fight_view.setup()
                self.window.show_view(fight_view)
            elif(GLOBAL_STATE == State.Swap):
                # Force the swap and then return to fight
                swap_view = PokemonSwap(self.player, self.enemy)
                swap_view.setup()
                self.window.show_view(swap_view)
                # print("fainted")
                # self.player.swap_pokemon(0, self.index)
                # GLOBAL_STATE = State.Battle
                # fight_view = PokemonGame(self.player, self.enemy)
                # fight_view.setup()
                # self.window.show_view(fight_view)
        else:
            self.player.swap_pokemon(0, self.index)
            GLOBAL_STATE = State.Battle
            fight_view = PokemonGame(self.player, self.enemy)
            fight_view.setup()
            self.window.show_view(fight_view)

    def on_draw(self):
            # Clear the screen
            self.clear()
    
            # Draw all the sprites.
            self.manager.draw()
            self.player_list.draw()

# This PokemonItem view class gives the fighter a chance to use items from their bag during the fight.
class PokemonItem(arcade.View):
    def __init__(self, player, enemy):
        super().__init__()
        self.player = player
        self.enemy = enemy
        self.pokemon = player.get_curr_pkm()
        self.state = State.Item

        # This variable keeps track of what item you are looking at
        self.index = 0

        # Background image will be stored in this variable
        self.background = None
        arcade.set_background_color(arcade.color.WHITE)

        # List of sprites for the items
        self.player_list = None

        # Button styling
        button_style = {
            "bg_color":(50,75,125),
            "bg_color_pressed":(20, 65, 115)
        }

        # Create "go back" button if the player doesn't want to use an item
        self.v_box = arcade.gui.UIBoxLayout()

        back_button = arcade.gui.UIFlatButton(text="Go Back", width=BUTTON_WIDTH * .75, style=button_style)
        self.v_box.add(back_button.with_space_around(bottom=20))
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

    def setup(self):
        # Create sprites for each of the items
        self.button_box_1 = arcade.gui.UIBoxLayout(vertical=False)

        self.player_list = arcade.SpriteList()
        self.item1_sprite = Sprite("../cs3050_pokemon/sprites/potion.png", .25 * SPRITE_SCALING)
        self.item1_sprite.center_x = SCREEN_WIDTH / 5
        self.item1_sprite.center_y = 3 * SCREEN_HEIGHT / 4
        self.player_list.append(self.item1_sprite)
        self.item1_text = arcade.create_text_sprite(
            start_x=SCREEN_WIDTH / 5,
            start_y=3 * SCREEN_HEIGHT / 4 - 50,
            color=arcade.color.BLACK,
            text = "Potion: " + str(self.player.amount_of_item(item_objects.potion)) + "x"
        )
        self.item1_text.center_x = SCREEN_WIDTH / 5
        self.item1_text.center_y = 3 * SCREEN_HEIGHT / 4 - 50
        self.player_list.append(self.item1_text)

        self.item2_sprite = Sprite("../cs3050_pokemon/sprites/super-potion.png", .25 * SPRITE_SCALING)
        self.item2_sprite.center_x = 2 * SCREEN_WIDTH / 5
        self.item2_sprite.center_y = 3 * SCREEN_HEIGHT / 4
        self.player_list.append(self.item2_sprite)
        self.item2_text = arcade.create_text_sprite(
            start_x=2 * SCREEN_WIDTH / 5,
            start_y=3 * SCREEN_HEIGHT / 4 - 50,
            color=arcade.color.BLACK,
            text = "Super Potion: " + str(self.player.amount_of_item(item_objects.super_potion)) + "x"
        )
        self.item2_text.center_x = 2 * SCREEN_WIDTH / 5
        self.item2_text.center_y = 3 * SCREEN_HEIGHT / 4 - 50
        self.player_list.append(self.item2_text)

        self.item3_sprite = Sprite("../cs3050_pokemon/sprites/hyper-potion.png", .25 * SPRITE_SCALING)
        self.item3_sprite.center_x = 3 * SCREEN_WIDTH / 5
        self.item3_sprite.center_y = 3 * SCREEN_HEIGHT / 4
        self.player_list.append(self.item3_sprite)
        self.item3_text = arcade.create_text_sprite(
            start_x=3 * SCREEN_WIDTH / 5,
            start_y=3 * SCREEN_HEIGHT / 4 - 50,
            color=arcade.color.BLACK,
            text = "Hyper Potion: " + str(self.player.amount_of_item(item_objects.hyper_potion)) + "x"
        )
        self.item3_text.center_x = 3 * SCREEN_WIDTH / 5
        self.item3_text.center_y = 3 * SCREEN_HEIGHT / 4 - 50
        self.player_list.append(self.item3_text)

        self.item4_sprite = Sprite("../cs3050_pokemon/sprites/max-potion.png", .25 * SPRITE_SCALING)
        self.item4_sprite.center_x = 4 * SCREEN_WIDTH / 5
        self.item4_sprite.center_y = 3 * SCREEN_HEIGHT / 4
        self.player_list.append(self.item4_sprite)
        self.item4_text = arcade.create_text_sprite(
            start_x=4 * SCREEN_WIDTH / 5,
            start_y=3 * SCREEN_HEIGHT / 4 - 50,
            color=arcade.color.BLACK,
            text = "Max Potion: " + str(self.player.amount_of_item(item_objects.max_potion)) + "x"
        )
        self.item4_text.center_x = 4 * SCREEN_WIDTH / 5
        self.item4_text.center_y = 3 * SCREEN_HEIGHT / 4 - 50
        self.player_list.append(self.item4_text)

        self.create_item_buttons()

    def back_button_action(self, event):
        # switch screen to fighting screen
        global GLOBAL_STATE
        if(GLOBAL_STATE == State.Item):
            print("returning to fight screen")
            GLOBAL_STATE = State.Battle
            fight_view = PokemonGame(self.player, self.enemy)
            fight_view.setup()
            self.window.show_view(fight_view)

    def create_item_buttons(self):
        # Create a button to use an item for each of the items in the dictionary with a value over 0
        if(int(self.player.amount_of_item(item_objects.potion) >= 1)):
            self.button1 = arcade.gui.UIFlatButton(text="Use", width=BUTTON_WIDTH / 2)
            self.button_box_1.add(self.button1.with_space_around(left=20))
            self.button1.on_click = self.use1
            self.manager.add(
                arcade.gui.UIAnchorWidget(align_x=SCREEN_WIDTH / 5 - SCREEN_WIDTH / 2, align_y=SCREEN_HEIGHT / 12,
                    anchor_x="center_x",
                    anchor_y="center_y",
                    child=self.button1)
            )
        if(int(self.player.amount_of_item(item_objects.super_potion) >= 1)):
            self.button2 = arcade.gui.UIFlatButton(text="Use", width=BUTTON_WIDTH / 2)
            self.button_box_1.add(self.button2.with_space_around(left=20))
            self.button2.on_click = self.use2
            self.manager.add(
                arcade.gui.UIAnchorWidget(align_x=2 * SCREEN_WIDTH / 5 - SCREEN_WIDTH / 2, align_y=SCREEN_HEIGHT / 12,
                    anchor_x="center_x",
                    anchor_y="center_y",
                    child=self.button2)
            )
        if(int(self.player.amount_of_item(item_objects.hyper_potion) >= 1)):
            self.button3 = arcade.gui.UIFlatButton(text="Use", width=BUTTON_WIDTH / 2)
            self.button_box_1.add(self.button3.with_space_around(left=20))
            self.button3.on_click = self.use3
            self.manager.add(
                arcade.gui.UIAnchorWidget(align_x= 3 * SCREEN_WIDTH / 5 - SCREEN_WIDTH / 2, align_y=SCREEN_HEIGHT / 12,
                    anchor_x="center_x",
                    anchor_y="center_y",
                    child=self.button3)
            )
        if(int(self.player.amount_of_item(item_objects.max_potion) >= 1)):
            self.button4 = arcade.gui.UIFlatButton(text="Use", width=BUTTON_WIDTH / 2)
            self.button_box_1.add(self.button4.with_space_around(left=20))
            self.button4.on_click = self.use4
            self.manager.add(
                arcade.gui.UIAnchorWidget(align_x=4 * SCREEN_WIDTH / 5 - SCREEN_WIDTH / 2, align_y=SCREEN_HEIGHT / 12,
                    anchor_x="center_x",
                    anchor_y="center_y",
                    child=self.button4)
            )

    def use1(self, event):
        self.index = "Potion"
        self.use()

    def use2(self, event):
        self.index = "Super Potion"
        self.use()
    
    def use3(self, event):
        self.index = "Hyper Potion"
        self.use()
    
    def use4(self, event):
        self.index = "Max Potion"
        self.use()
    
    def use(self):
        # Call battle function with the request to use an item
        global GLOBAL_STATE
        if(GLOBAL_STATE == State.Item):
            btn_info = []
            if(self.index == "Potion"):
                btn_info = ["item", item_objects.potion]
            elif(self.index == "Super Potion"):
                btn_info = ["item", item_objects.super_potion]
            elif(self.index == "Hyper Potion"):
                btn_info = ["item", item_objects.hyper_potion]
            elif(self.index == "Max Potion"):
                btn_info = ["item", item_objects.max_potion]
            action1, action2 = battle(self.player, self.enemy, btn_info)
            
            print("using " + self.index)
            GLOBAL_STATE = State.Battle
            # Return to the fight view
            fight_view = PokemonGame(self.player, self.enemy)
            fight_view.setup()
            self.window.show_view(fight_view)


    def on_draw(self):
            # Clear the screen
            self.clear()

            # Draw all the sprites.
            self.manager.draw()
            self.player_list.draw()

# This PokemonStats view class displays the sprite of the selected pokemon along with their stats relating to
# health, attacking, moves, etc.
class PokemonStats(arcade.View):
    def __init__(self, player, enemy, pokemon):
        super().__init__()
        self.pokemon = pokemon
        self.player = player
        self.enemy = enemy
        self.state = State.Stat

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
        global GLOBAL_STATE
        if(GLOBAL_STATE == State.Stat):
            print("returning to swap screen")
            GLOBAL_STATE = State.Swap
            swap_view = PokemonSwap(self.player, self.enemy)
            swap_view.setup()
            self.window.show_view(swap_view)

    def on_draw(self):
            # Clear the screen
            self.clear()
        
            # Draw all the sprites.
            self.manager.draw()
            self.player_list.draw()


# This PokemonRules view class displays a scrollable textbox with the information on how to play the game.
# It has a button to return to the start screen that renders the PokemonStart view.
class PokemonRules(arcade.View):
    def __init__(self, player, enemy):
        super().__init__()
        self.player = player
        self.enemy = enemy
        self.state = State.Rules

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
        # TODO: create any sprites needed for rules page
        print("setting up rules")

    def back_button_action(self, event):
        #TODO: switch screen to starting screen
        global GLOBAL_STATE
        if(GLOBAL_STATE == State.Rules):
            print("returning to start screen")
            GLOBAL_STATE = State.Start
            start_view = PokemonStart(self.player, self.enemy)
            start_view.setup()
            self.window.show_view(start_view)


    def on_draw(self):
            # Clear the screen
            self.clear()
        
            # Draw all the sprites.
            self.manager.draw()

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
    def __init__(self, player, enemy):
        super().__init__()
        # Start in the battle state for deliverable 1
        self.state = State.Battle
        self.player = player
        self.enemy = enemy

        # Background image will be stored in this variable
        self.background = None

        #TODO: FOR TESTING PURPOSES, this overrides the original health of the pokemon object
        #self.player.get_curr_pkm().set_curr_hlth(1000)

        # Health bar
        self.bar_sprite_list = arcade.SpriteList()
        self.enemy_health_bar = HealthBar(self.enemy.get_curr_pkm(), self.bar_sprite_list, 350, 500, 515)
        self.player_health_bar = HealthBar(self.player.get_curr_pkm(), self.bar_sprite_list, 550, 250, 265)

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
            arcade.gui.UIAnchorWidget(align_x=V_BOX_X, align_y= V_BOX_Y,
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box)
        )

        # Create a widget to hold the v_box_2 widget, that will center the buttons
        self.manager.add(
            arcade.gui.UIAnchorWidget(align_x=V_BOX_2_X, align_y= V_BOX_2_Y,
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box_2)
        )

    # This fight_action method is called when the fight button is clicked, it changes the state and adds new buttons
    def fight_action(self, event):
        global GLOBAL_STATE
        if(GLOBAL_STATE == State.Battle):
            GLOBAL_STATE = State.Moves
            self.state = State.Moves
            self.add_move_buttons()
            self.on_draw()

    def pokemon_button_action(self, event):
        global GLOBAL_STATE
        if(GLOBAL_STATE == State.Battle):
            self.state = State.PokemonSwap
            GLOBAL_STATE = State.Swap
            # TODO: Call method to render sprites to swap with
            start_view = PokemonSwap(self.player, self.enemy)
            start_view.setup()
            self.window.show_view(start_view)

    def items_button_action(self, event):
        global GLOBAL_STATE
        if(GLOBAL_STATE == State.Battle):
            self.state = State.Bag
            GLOBAL_STATE = State.Item
            bag_view = PokemonItem(self.player, self.enemy)
            bag_view.setup()
            self.window.show_view(bag_view)

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
        """ Render the screen. """
        #print(self.player.get_curr_pkm().get_name())
        # print(self.player.chk_party())
        if(self.state == State.Battle):
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
        if(self.state == State.PokemonSwap):
            self.clear()
            # Iterate through pokemon in party and display the sprites on screen
            # If you click on a sprite, it will swap and return to the battle screen
            # Give an option to check summary stats or click swap (called from pokemon_button onclick function)
        if(self.state == State.Bag):
            self.clear()

        # When the backend determines the enemy has been defeated, change states
        if not self.enemy.chk_party():
            self.state = State.Win
        if not self.player.chk_party():
            self.state = State.Loss

        
        if(self.state == State.Moves):
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
        if(self.state == State.Win):
            self.clear()
            self.bar_sprite_list.clear()

            # TODO: Set up a winning screen for later deliverables
            arcade.set_background_color(arcade.color.RED)
            self.health_text = arcade.create_text_sprite (
                start_x=350,
                start_y=500,
                color=arcade.color.BLACK,
                text = "WIN"
            )
            self.health_text.center_x = 350
            self.health_text.center_y = 500
            self.bar_sprite_list.append(self.health_text)
            self.bar_sprite_list.draw()
        if(self.state == State.Loss):
            self.clear()
            self.bar_sprite_list.clear()

            # TODO: Set up a winning screen for later deliverables
            arcade.set_background_color(arcade.color.BLUE)
            self.health_text = arcade.create_text_sprite (
                start_x=350,
                start_y=500,
                color=arcade.color.BLACK,
                text = "LOSS"
            )
            self.health_text.center_x = 350
            self.health_text.center_y = 500
            self.bar_sprite_list.append(self.health_text)
            self.bar_sprite_list.draw()

        #should be handling weird swap case
        if(self.player.get_curr_pkm().get_is_fainted() and self.player.chk_party()):
            print("current player pokemon fainted - swap pokemon")
            # Render swap screen so they can switch.
            self.state = State.PokemonSwap
            global GLOBAL_STATE
            GLOBAL_STATE = State.Swap
            # TODO: Call method to render sprites to swap with
            start_view = PokemonSwap(self.player, self.enemy)
            start_view.setup()
            self.window.show_view(start_view)
    # This add_move_buttons methis is called from the fight on_click method and adds the move buttons to
    # the vertical box storing the window's buttons. 
    def add_move_buttons(self):
        self.v_box.clear()
        self.v_box_2.clear()
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

    # This add_move_buttons methis is called from the fight on_click method and adds the move buttons to
    # the vertical box storing the window's buttons. 
    def remove_move_buttons(self):
        # Remove move button widgets
        self.v_box.clear()
        self.v_box_2.clear()
        # Create two vertical BoxGroup widges to align buttons
        self.v_box = arcade.gui.UIBoxLayout()
        self.v_box_2 = arcade.gui.UIBoxLayout()

        # Fight button to access the moves
        fight = arcade.gui.UIFlatButton(text="Fight", width=BUTTON_WIDTH)
        self.v_box.add(fight.with_space_around(bottom=20))
        fight.on_click = self.fight_action

        # Look at your pokemon and swap
        pokemon_button = arcade.gui.UIFlatButton(text="Pokemon", width=BUTTON_WIDTH)
        self.v_box.add(pokemon_button.with_space_around(bottom=20))
        pokemon_button.on_click = self.pokemon_button_action

        # Bag button to access items
        items_button = arcade.gui.UIFlatButton(text="Items", width=BUTTON_WIDTH)
        self.v_box_2.add(items_button.with_space_around(bottom=20))
        items_button.on_click = self.items_button_action

        # Create widgets to hold the v_box and v_box_2 widgets, that will center the buttons
        self.manager.add(
            arcade.gui.UIAnchorWidget(align_x=V_BOX_X, align_y= V_BOX_Y,
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box)
        )
        self.manager.add(
            arcade.gui.UIAnchorWidget(align_x=V_BOX_2_X, align_y= V_BOX_2_Y,
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box_2)
        )

    # This move_1_go method is called when the first move button is clicked, it passes button information
    # to the backend where the battle function is called. The results of the tern are reflected in the 
    # HealthBar Sprites
    def move_1_go(self, event):
        global GLOBAL_STATE
        if(GLOBAL_STATE == State.Moves):
            print("accessing first move")
            GLOBAL_STATE = State.Battle

            # TODO: Add some sort of movement for sprite when move is performed
            self.move_1_animate()

            btn_info = ["move", self.player.get_curr_pkm().get_moves()[0]]
            action1, action2 = battle(self.player, self.enemy, btn_info)
            if(self.enemy.get_curr_pkm().get_is_fainted()):
                # Render the fight screen again with the updated sprite
                fight_view = PokemonGame(self.player, self.enemy)
                fight_view.setup()
                self.window.show_view(fight_view)
            # Reflects changes in the sprite of the healthbar
            self.enemy_health_bar.health_bar_update(self.bar_sprite_list)
            self.player_health_bar.health_bar_update(self.bar_sprite_list)
            if(action1 != "win"):
                # Render the fight screen again with the updated sprite
                fight_view = PokemonGame(self.player, self.enemy)
                fight_view.setup()
                self.window.show_view(fight_view)
            else:
                GLOBAL_STATE = State.Win
                self.state = State.Win

    # This move_2_go method is called when the second move button is clicked, it passes button information
    # to the backend where the battle function is called. The results of the tern are reflected in the 
    # HealthBar Sprites
    def move_2_go(self, event):
        global GLOBAL_STATE
        if(GLOBAL_STATE == State.Moves):
            GLOBAL_STATE = State.Battle
            print("accessing second move")
            btn_info = ["move", self.player.get_curr_pkm().get_moves()[1]]
            action1, action2 = battle(self.player, self.enemy, btn_info)
            if(self.enemy.get_curr_pkm().get_is_fainted()):
                # Render the fight screen again with the updated sprite
                fight_view = PokemonGame(self.player, self.enemy)
                fight_view.setup()
                self.window.show_view(fight_view)
            self.enemy_health_bar.health_bar_update(self.bar_sprite_list)
            self.player_health_bar.health_bar_update(self.bar_sprite_list)

            if(action1 != "win"):
                # Render the fight screen again with the updated sprite
                fight_view = PokemonGame(self.player, self.enemy)
                fight_view.setup()
                self.window.show_view(fight_view)
            else:
                GLOBAL_STATE = State.Win
                self.state = State.Win
            

    # This move_3_go method is called when the third move button is clicked, it passes button information
    # to the backend where the battle function is called. The results of the tern are reflected in the 
    # HealthBar Sprites
    def move_3_go(self, event):
        global GLOBAL_STATE
        if(GLOBAL_STATE == State.Moves):
            GLOBAL_STATE = State.Battle
            print("accessing third move")
            btn_info = ["move", self.player.get_curr_pkm().get_moves()[2]]
            action1, action2 = battle(self.player, self.enemy, btn_info)
            if(self.enemy.get_curr_pkm().get_is_fainted()):
                # Render the fight screen again with the updated sprite
                fight_view = PokemonGame(self.player, self.enemy)
                fight_view.setup()
                self.window.show_view(fight_view)
            self.enemy_health_bar.health_bar_update(self.bar_sprite_list)
            self.player_health_bar.health_bar_update(self.bar_sprite_list)

            if(action1 != "win"):
                # Render the fight screen again with the updated sprite
                fight_view = PokemonGame(self.player, self.enemy)
                fight_view.setup()
                self.window.show_view(fight_view)
            else:
                GLOBAL_STATE = State.Win
                self.state = State.Win

    # This move_4_go method is called when the fourth move button is clicked, it passes button information
    # to the backend where the battle function is called. The results of the tern are reflected in the 
    # HealthBar Sprites
    def move_4_go(self, event):
        global GLOBAL_STATE
        if(GLOBAL_STATE == State.Moves):
            GLOBAL_STATE = State.Battle
            print("accessing fourth move")
            btn_info = ["move", self.player.get_curr_pkm().get_moves()[3]]
            action1, action2 = battle(self.player, self.enemy, btn_info)
            if(self.enemy.get_curr_pkm().get_is_fainted()):
                # Render the fight screen again with the updated sprite
                fight_view = PokemonGame(self.player, self.enemy)
                fight_view.setup()
                self.window.show_view(fight_view)
            self.enemy_health_bar.health_bar_update(self.bar_sprite_list)
            self.player_health_bar.health_bar_update(self.bar_sprite_list)

            if(action1 != "win"):
                # Render the fight screen again with the updated sprite
                fight_view = PokemonGame(self.player, self.enemy)
                fight_view.setup()
                self.window.show_view(fight_view)
            else:
                GLOBAL_STATE = State.Win
                self.state = State.Win

    # This move_1_animate method is for future deliverables and will animate the sprite when a turn is processed
    def move_1_animate(self):
        # TODO: make the sprite move with the update function
        self.move_up = True
        self.animate = True

    # This update_player_speed method checks keybard input and reflects the movement speed of the player.
    # Movement will be implemented in a later deliverable.
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

    # This on_update method is called each frame of the game and calls the respective update methods of the sprites
    def on_update(self, delta_time):
        """ Movement and game logic """
        # Call update to move the sprite
        self.player_list.update()
        self.enemy_list.update()
        self.bar_sprite_list.update()

    # This on_key_press method listens for keyboard input
    def on_key_press(self, key, modifiers):
        """Listen for a key press from user """

        if(self.state == State.World):
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

    # This on_key_release method listens for keyboard input
    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if(self.state == State.World):
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

# This main function creates two pokemon bags, two Character objects, and passes them
# to the PokemonGame object and renders the window to run the game.
def main():
    """ Main function """
    pokemon_bag_user = [pokemon_objects.pikachu, pokemon_objects.charizard, pokemon_objects.bulbasaur]
    user_item_bag = {item_objects.potion: 1, item_objects.super_potion: 1, item_objects.hyper_potion: 1,
                        item_objects.max_potion: 1}
    

    pokemon_bag_enemy = [pokemon_objects.enemy_charizard, pokemon_objects.enemy_gengar, pokemon_objects.enemy_pidgeotto]
    enemy_item_bag = {item_objects.potion: 1, item_objects.super_potion: 1, item_objects.hyper_potion: 1,
                      item_objects.max_potion: 1}

    user_trainer = Character("Ash", pokemon_bag_user, user_item_bag, 1000,
                              "I'm on a journey to become a Pokemon Master!")
    enemy_trainer = Character("Misty", pokemon_bag_enemy, enemy_item_bag, 800, "Water types are the best!")

    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, B_SCREEN_TITLE)

    start_view = PokemonStart(user_trainer, enemy_trainer)
    window.show_view(start_view)
    start_view.setup()

    arcade.run()

if __name__ == "__main__":
    main()
