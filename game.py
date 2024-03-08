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
import time

# Enum to hold the current state of the game, used to update the screen rendering
class State(Enum):
    Start = 1
    World = 2
    Battle = 3
    Moves = 4
    Win = 5

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

BUTTON_WIDTH = 175

# Possible TODOs
# Create subclass for the user
# Subclass for pokemon
# Subclass for enemy

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
            text = str(self.health) + " / " + str(self.max_health)
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
        self.health_text = arcade.create_text_sprite (
            start_x=self.pos_x,
            start_y=self.pos_y,
            color=arcade.color.BLACK,
            text = str(self.health) + " / " + str(self.max_health)
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

# This PokemonGame class is created with two trainers passed in, the player and the enemy trainer
# the pokemon bags of each trainer are represented on the screen with Sprites and health_bar sprites.
class PokemonGame(arcade.Window):
    """
    constructor for PokemonGame class 
    attributes of class
    width - width of the screen in pixels - int
    height - heigth of the screen in pixels - int
    title - the name of the screen - string
    player - Character object representing the player - Character
    enemy - Character object representing the enemy trainer - Character
    """
    def __init__(self, width, height, title, player, enemy):
        super().__init__(width, height, title)
        # Start in the battle state for deliverable 1
        self.state = State.Battle
        self.player = player
        self.enemy = enemy

        # Background image will be stored in this variable
        self.background = None

        #TODO: FOR TESTING PURPOSES, this overrides the original health of the pokemon object
        self.player.get_curr_pkm().set_curr_hlth(1000)

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
        text_area = UITextArea(x=0,
                               y=0,
                               width=SCREEN_WIDTH / 2,
                               height=SCREEN_HEIGHT / 4,
                               text="What will " + self.player.get_curr_pkm().get_name() + " do?",
                               font_size=FONT_SIZE,
                               text_color=arcade.color.BLACK)
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

        # Create the buttons (later deliverables will have bag/run as options too)
        fight = arcade.gui.UIFlatButton(text="Fight", width=200)
        self.v_box.add(fight.with_space_around(bottom=20))

        # assign self.fight_action as callback
        fight.on_click = self.fight_action

        # Create a widget to hold the v_box widget, that will center the buttons
        self.manager.add(
            arcade.gui.UIAnchorWidget(align_x=100, align_y= -200,
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box)
        )

    # This fight_action method is called when the fight button is clicked, it changes the state and adds new buttons
    def fight_action(self, event):
        self.state = State.Moves
        self.add_move_buttons()
        self.on_draw()

    # This setup method is called when creating all the sprites to be stored on the screen when the window is rendered
    def setup(self):
        """ Set up the game and initialize the variables. """
        # Sprite lists
        self.player_list = arcade.SpriteList()
    
        # Set up the player and enemy sprites
        self.player_sprite = Sprite("../cs3050_pokemon/sprites/" + self.player.get_curr_pkm().get_name().lower() + "-back.png", SPRITE_SCALING)
        self.player_sprite2 = Sprite("../cs3050_pokemon/sprites/" + self.enemy.get_curr_pkm().get_name().lower() + "-front.png", OPPONENT_SPRITE_SCALING)
        # TODO: change these to constant variables
        self.player_sprite.center_x = 200
        self.player_sprite.center_y = 235
        self.player_sprite2.center_x = 600
        self.player_sprite2.center_y = 725
        self.player_list.append(self.player_sprite)
        self.player_list.append(self.player_sprite2)
        self.background = arcade.load_texture("../cs3050_pokemon/images/fight-background.png")
    
    # This on_draw method renders all of the buttons and sprites depending on what the current state is
    def on_draw(self):
        """ Render the screen. """
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
            self.bar_sprite_list.draw()
        # When the backend determines the enemy has been defeated, change states
        if(self.enemy.get_curr_pkm().get_is_fainted()):
            self.state = State.Win
        if(self.state == State.Moves):
            self.clear()
            # Draw the background texture
            arcade.draw_lrwh_rectangle_textured(0, 150,
                                            SCREEN_WIDTH, SCREEN_HEIGHT,
                                            self.background)
            # Draw the sprites
            self.manager.draw()
            self.player_list.draw()
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

    # This add_move_buttons methis is called from the fight on_click method and adds the move buttons to
    # the vertical box storing the window's buttons. 
    def add_move_buttons(self):
        self.v_box.clear()
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
            arcade.gui.UIAnchorWidget(align_x=100, align_y= -225,
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box)
        )
        self.manager.add(
            arcade.gui.UIAnchorWidget(align_x=300, align_y= -225,
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box_2)
        )

    # This move_1_go method is called when the first move button is clicked, it passes button information
    # to the backend where the battle function is called. The results of the tern are reflected in the 
    # HealthBar Sprites
    def move_1_go(self, event):
        print("accessing first move")

        # TODO: Add some sort of movement for sprite when move is performed
        self.move_1_animate()

        btn_info = ["move", self.player.get_curr_pkm().get_moves()[0]]
        action1, action2 = battle(self.player, self.enemy, btn_info)

        # Reflects changes in the sprite of the healthbar
        self.enemy_health_bar.health_bar_update(self.bar_sprite_list)
        self.player_health_bar.health_bar_update(self.bar_sprite_list)

    # This move_2_go method is called when the second move button is clicked, it passes button information
    # to the backend where the battle function is called. The results of the tern are reflected in the 
    # HealthBar Sprites
    def move_2_go(self, event):
        print("accessing second move")
        btn_info = ["move", self.player.get_curr_pkm().get_moves()[1]]
        battle(self.player, self.enemy, btn_info)
        self.enemy_health_bar.health_bar_update(self.bar_sprite_list)
        self.player_health_bar.health_bar_update(self.bar_sprite_list)

    # This move_3_go method is called when the third move button is clicked, it passes button information
    # to the backend where the battle function is called. The results of the tern are reflected in the 
    # HealthBar Sprites
    def move_3_go(self, event):
        print("accessing third move")
        btn_info = ["move", self.player.get_curr_pkm().get_moves()[2]]
        battle(self.player, self.enemy, btn_info)
        self.enemy_health_bar.health_bar_update(self.bar_sprite_list)
        self.player_health_bar.health_bar_update(self.bar_sprite_list)

    # This move_4_go method is called when the fourth move button is clicked, it passes button information
    # to the backend where the battle function is called. The results of the tern are reflected in the 
    # HealthBar Sprites
    def move_4_go(self, event):
        print("accessing fourth move")
        btn_info = ["move", self.player.get_curr_pkm().get_moves()[3]]
        battle(self.player, self.enemy, btn_info)
        self.enemy_health_bar.health_bar_update(self.bar_sprite_list)
        self.player_health_bar.health_bar_update(self.bar_sprite_list)

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
    pokemon_bag = [pokemon_objects.bulbasaur, pokemon_objects.charizard]
    trainer1 = Character("Ash", pokemon_bag, [], 1000,
                              "I'm on a journey to become a Pokemon Master!")
    pokemon_bag_trainer2 = [pokemon_objects.charizard]
    trainer2 = Character("Misty", pokemon_bag_trainer2, [], 800, "Water types are the best!")

    window = PokemonGame(SCREEN_WIDTH, SCREEN_HEIGHT, B_SCREEN_TITLE, trainer1, trainer2)
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()
