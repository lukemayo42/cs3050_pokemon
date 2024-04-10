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
from state import State
from views.health import Sprite
from views.button import CustomButton

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TOP_ROW = 2 * SCREEN_HEIGHT / 3 + (SCREEN_HEIGHT / 8)
BOTTOM_ROW = SCREEN_HEIGHT / 3 + (SCREEN_HEIGHT / 8)

FONT_SIZE = 20

SPRITE_SCALING = 3.5
OPPONENT_SPRITE_SCALING = 3
PAGE_SIZE = 8

# Button formatting
BUTTON_WIDTH = 175

class PokemonParty(arcade.View):
    def __init__(self, player, enemy, pokemon_list, state):
        super().__init__()
        self.state = state
        self.player = player
        self.enemy = enemy
        self.pokemon_list = pokemon_list

        self.background = None
        self.sprite_list = arcade.SpriteList()
        arcade.set_background_color(arcade.color.WHITE)

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

        # Create "next page" button
        self.v_box_2 = arcade.gui.UIBoxLayout()
        next_page_button = arcade.gui.UIFlatButton(text="Next page", width=BUTTON_WIDTH * .75, style=button_style)
        self.v_box_2.add(next_page_button.with_space_around(bottom=20))

        # Assign self.items_button as a callback to render item bag
        next_page_button.on_click = self.next_page_action

        self.manager = UIManager()
        self.manager.enable()
        # Create a widget to hold the v_box widget, that will center the buttons
        self.manager.add(
            arcade.gui.UIAnchorWidget(align_x=-SCREEN_WIDTH / 3, align_y= -SCREEN_HEIGHT / 2.5,
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box)
        )
        if(self.state.get_state().value != State.Party2.value):
            self.manager.add(
                arcade.gui.UIAnchorWidget(align_x=SCREEN_WIDTH / 3, align_y= -SCREEN_HEIGHT / 2.5,
                    anchor_x="center_x",
                    anchor_y="center_y",
                    child=self.v_box_2)
            )
        # Add name/stats for pokemon
        self.header_text = arcade.create_text_sprite (
            start_x=SCREEN_WIDTH / 4,
            start_y=SCREEN_HEIGHT / 2,
            color=arcade.color.BLACK,
            text = "Choose your party!"
        )
    def setup(self):
        self.background_sky = arcade.load_texture("../cs3050_pokemon/images/screen_background.png")
        start = 0
        end = 0
        if(self.state.get_state().value == State.Party.value):
            if(len(self.pokemon_list) >= PAGE_SIZE):
                end = PAGE_SIZE
            else:
                end = len(self.pokemon_list)
        elif(self.state.get_state().value == State.Party2.value):
            start = PAGE_SIZE
            if(len(self.pokemon_list) >= PAGE_SIZE * 2):
                end = 2 * PAGE_SIZE
            else:
                end = len(self.pokemon_list)
        for i in range(start, end):
            sprite = Sprite("../cs3050_pokemon/sprites/" + self.pokemon_list[i].get_name().lower() + "-front.png")
            sprite.scale = SCREEN_HEIGHT / (sprite.height * 5)
            
            # TODO: Have both x and y be based on i so it goes across the page
            # Even i will be top row, odd will be bottom row
            if(self.state.get_state().value == State.Party.value):
                if(i % 2 == 0):
                    sprite.center_x = (SCREEN_WIDTH / 8) + (i * (SCREEN_WIDTH / 8))
                    sprite.center_y = TOP_ROW
                else:
                    sprite.center_x = (i * (SCREEN_WIDTH / 8))
                    sprite.center_y = BOTTOM_ROW
            else:
                if(i % 2 == 0):
                    sprite.center_x = (SCREEN_WIDTH / 8) + ((i - 8) * (SCREEN_WIDTH / 8))
                    sprite.center_y = TOP_ROW
                else:
                    sprite.center_x = ((i - 8) * (SCREEN_WIDTH / 8))
                    sprite.center_y = BOTTOM_ROW
            # sprite.center_x = SCREEN_HEIGHT
            # sprite.center_y = i * SCREEN_WIDTH / 3.2
            self.sprite_list.append(sprite)

            # Add the pokemon name to the list of sprites to render
            name = arcade.create_text_sprite (
                start_x=SCREEN_HEIGHT,
                start_y=i * SCREEN_WIDTH / 3.2,
                color=arcade.color.BLACK,
                text = str(self.pokemon_list[i].get_name())
            )
            name.center_x = sprite.center_x
            name.center_y = sprite.bottom - SCREEN_HEIGHT / 30

            self.sprite_list.append(name)
            # if(self.pokemon_list[i] in self.player.get_pokemon_list()):
            if(i % 2 == 0):
                self.create_choices(i, sprite.center_x, .85 * TOP_ROW, self.pokemon_list[i] in self.player.get_pokemon_list())
            else:
                self.create_choices(i, sprite.center_x, 2*BOTTOM_ROW/3, self.pokemon_list[i] in self.player.get_pokemon_list())
            # TODO: Call function to render buttons for the sprite
            # self.create_party_options(SCREEN_HEIGHT, sprite.bottom - SCREEN_HEIGHT / 30, i == 1, self.pokemon_list[i].get_is_fainted())

    def create_choices(self, index, pos_x, pos_y, in_party):
        button_box = arcade.gui.UIBoxLayout(vertical=False)
        stats_button = arcade.gui.UIFlatButton(text="Stats", width=BUTTON_WIDTH / 2)
        button_box.add(stats_button.with_space_around(left=10))
        # TODO: THis is ridiculous how do I dynamically create the on click method??
        if(index == 0):
            stats_button.on_click = self.generate_stats_view_1
        elif(index == 1):
            stats_button.on_click = self.generate_stats_view_2
        elif(index == 2):
            stats_button.on_click = self.generate_stats_view_3
        elif(index == 3):
            stats_button.on_click = self.generate_stats_view_4
        elif(index == 4):
            stats_button.on_click = self.generate_stats_view_5
        elif(index == 5):
            stats_button.on_click = self.generate_stats_view_6
        elif(index == 6):
            stats_button.on_click = self.generate_stats_view_7
        elif(index == 7):
            stats_button.on_click = self.generate_stats_view_8
        elif(index == 8):
            stats_button.on_click = self.generate_stats_view_9
        elif(index == 9):
            stats_button.on_click = self.generate_stats_view_10
        elif(index == 10):
            stats_button.on_click = self.generate_stats_view_11
        elif(index == 11):
            stats_button.on_click = self.generate_stats_view_12
        elif(index == 12):
            stats_button.on_click = self.generate_stats_view_13
        elif(index == 13):
            stats_button.on_click = self.generate_stats_view_14
        elif(index == 14):
            stats_button.on_click = self.generate_stats_view_15
        elif(index == 15):
            stats_button.on_click = self.generate_stats_view_16
        
        if(not in_party):
            add_button = arcade.gui.UIFlatButton(text="Add to Party", width=BUTTON_WIDTH / 2)
            button_box.add(add_button.with_space_around(left=10))
            if(index == 0):
                add_button.on_click = self.add_action_1
            elif(index == 1):
                add_button.on_click = self.add_action_2
            elif(index == 2):
                add_button.on_click = self.add_action_3
            elif(index == 3):
                add_button.on_click = self.add_action_4
            elif(index == 4):
                add_button.on_click = self.add_action_5
            elif(index == 5):
                add_button.on_click = self.add_action_6
            elif(index == 6):
                add_button.on_click = self.add_action_7
            elif(index == 7):
                add_button.on_click = self.add_action_8
            elif(index == 8):
                add_button.on_click = self.add_action_9
            elif(index == 9):
                add_button.on_click = self.add_action_10
            elif(index == 10):
                add_button.on_click = self.add_action_11
            elif(index == 11):
                add_button.on_click = self.add_action_12
            elif(index == 12):
                add_button.on_click = self.add_action_13
            elif(index == 13):
                add_button.on_click = self.add_action_14
            elif(index == 14):
                add_button.on_click = self.add_action_15
            elif(index == 15):
                add_button.on_click = self.add_action_16
            
        # Create widgets to hold the button_box_1 widgets, that will center the buttons
        self.manager.add(
            arcade.gui.UIAnchorWidget(align_x=pos_x - SCREEN_WIDTH / 2, align_y=(pos_y - (SCREEN_HEIGHT / 20)) - SCREEN_HEIGHT / 2, 
                anchor_x="center_x",
                anchor_y="center_y",
                child=button_box)
        )

    def back_button_action(self, event):
        # switch screen to start screen
        if(self.state.get_state().value == State.Party.value):
            print("returning to start screen")
            self.state.set_state(State.Start)
            self.state.set_rendered(False)
        elif(self.state.get_state().value == State.Party2.value):
            self.state.set_state(State.Party)
            self.state.set_rendered(False)
    def next_page_action(self, event):
        if(self.state.get_state().value == State.Party.value):
            self.state.set_state(State.Party2)
            self.state.set_rendered(False)


    def generate_stats_view_1(self, event):
        self.index = 0
        self.state.set_user_choice(self.index)
        self.generate_stats()
    def generate_stats_view_2(self, event):
        self.index = 1
        self.state.set_user_choice(self.index)
        self.generate_stats()
    def generate_stats_view_3(self, event):
        self.index = 2
        self.state.set_user_choice(self.index)
        self.generate_stats()
    def generate_stats_view_4(self, event):
        self.index = 3
        self.state.set_user_choice(self.index)
        self.generate_stats()
    def generate_stats_view_5(self, event):
        self.index = 4
        self.state.set_user_choice(self.index )
        self.generate_stats()
    def generate_stats_view_6(self, event):
        self.index = 5
        self.state.set_user_choice(self.index)
        self.generate_stats()
    def generate_stats_view_7(self, event):
        self.index = 6
        self.state.set_user_choice(self.index)
        self.generate_stats()
    def generate_stats_view_8(self, event):
        self.index = 7
        self.state.set_user_choice(self.index)
        self.generate_stats()
    def generate_stats_view_9(self, event):
        self.index = 8
        self.state.set_user_choice(self.index)
        self.generate_stats()
    def generate_stats_view_10(self, event):
        self.index = 9
        self.state.set_user_choice(self.index)
        self.generate_stats()
    def generate_stats_view_11(self, event):
        self.index = 10
        self.state.set_user_choice(self.index)
        self.generate_stats()
    def generate_stats_view_12(self, event):
        self.index = 11
        self.state.set_user_choice(self.index)
        self.generate_stats()
    def generate_stats_view_13(self, event):
        self.index = 12
        self.state.set_user_choice(self.index)
        self.generate_stats()
    def generate_stats_view_14(self, event):
        self.index = 13
        self.state.set_user_choice(self.index)
        self.generate_stats()
    def generate_stats_view_15(self, event):
        self.index = 14
        self.state.set_user_choice(self.index)
        self.generate_stats()
    def generate_stats_view_16(self, event):
        self.index = 15
        self.state.set_user_choice(self.index)
        self.generate_stats()

    def add_action_1(self, event):
        self.index = 0
        self.state.set_user_choice(self.index)
        self.add_pokemon(self.index)
    def add_action_2(self, event):
        self.index = 1
        self.state.set_user_choice(self.index)
        self.add_pokemon(self.index)
    def add_action_3(self, event):
        self.index = 2
        self.state.set_user_choice(self.index)
        self.add_pokemon(self.index)
    def add_action_4(self, event):
        self.index = 3
        self.state.set_user_choice(self.index)
        self.add_pokemon(self.index)
    def add_action_5(self, event):
        self.index = 4
        self.state.set_user_choice(self.index)
        self.add_pokemon(self.index)
    def add_action_6(self, event):
        self.index = 5
        self.state.set_user_choice(self.index)
        self.add_pokemon(self.index)
    def add_action_7(self, event):
        self.index = 6
        self.state.set_user_choice(self.index)
        self.add_pokemon(self.index)
    def add_action_8(self, event):
        self.index = 7
        self.state.set_user_choice(self.index)
        self.add_pokemon(self.index)
    def add_action_9(self, event):
        self.index = 8
        self.state.set_user_choice(self.index)
        self.add_pokemon(self.index)
    def add_action_10(self, event):
        self.index = 9
        self.state.set_user_choice(self.index)
        self.add_pokemon(self.index)
    def add_action_11(self, event):
        self.index = 10
        self.state.set_user_choice(self.index)
        self.add_pokemon(self.index)
    def add_action_12(self, event):
        self.index = 11
        self.state.set_user_choice(self.index)
        self.add_pokemon(self.index)
    def add_action_13(self, event):
        self.index = 12
        self.state.set_user_choice(self.index)
        self.add_pokemon(self.index)
    def add_action_14(self, event):
        self.index = 13
        self.state.set_user_choice(self.index)
        self.add_pokemon(self.index)
    def add_action_15(self, event):
        self.index = 14
        self.state.set_user_choice(self.index)
        self.add_pokemon(self.index)
    def add_action_16(self, event):
        self.index = 15
        self.state.set_user_choice(self.index)
        self.add_pokemon(self.index)
    
    def generate_stats(self):
        # Get the selected pokemon and pass it to the stats view
        pokemon = self.pokemon_list[self.index]
        print(pokemon.get_name())
        if(self.state.get_state().value == State.Party.value):
            print("going to stats screen")
            self.state.set_state(State.PartyStat)
            self.state.set_rendered(False)
        if(self.state.get_state().value == State.Party2.value):
            print("going to stats screen")
            self.state.set_state(State.PartyStat2)
            self.state.set_rendered(False)
    def add_pokemon(self, index):
        if(self.state.get_state().value == State.Party.value):
            pokemon = self.pokemon_list[self.index]
            self.player.add_pokemon(pokemon)
            self.state.set_state(State.Party)
            self.state.set_rendered(False)
        elif(self.state.get_state().value == State.Party2.value):
            pokemon = self.pokemon_list[self.index]
            self.player.add_pokemon(pokemon)
            self.state.set_state(State.Party2)
            self.state.set_rendered(False)


    def on_draw(self):
            # Clear the screen
            self.clear()
            arcade.draw_lrwh_rectangle_textured(0, 0,
                                                SCREEN_WIDTH, SCREEN_HEIGHT,
                                                self.background_sky)
        
            # Draw all the sprites.
            self.manager.draw()
            self.sprite_list.draw()
    def on_update(self, delta_time):
        if(len(self.player.get_pokemon_list()) == 3):
            self.state.set_state(State.World)
            self.state.set_rendered(False)
        for pokemon in self.player.get_pokemon_list():
            print(pokemon.get_name())