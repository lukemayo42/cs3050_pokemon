import arcade
import arcade.gui
from arcade.gui import UIManager
from battle import battle
import item_objects

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

# This PokemonItem view class gives the fighter a chance to use items from their bag during the fight.
class PokemonItem(arcade.View):
    def __init__(self, player, enemy, state):
        super().__init__()
        self.player = player
        self.enemy = enemy
        self.pokemon = player.get_curr_pkm()
        self.state = state

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
        self.background_sky = arcade.load_texture("../cs3050_pokemon/images/screen_background.png")
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
        if(self.state.get_state().value == State.Item.value):
            print("returning to fight screen")
            self.state.set_state(State.Battle)
            self.state.set_rendered(False)

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
        if(self.state.get_state().value == State.Item.value):
            btn_info = []
            if(self.index == "Potion"):
                btn_info = ["item", item_objects.potion]
            elif(self.index == "Super Potion"):
                btn_info = ["item", item_objects.super_potion]
            elif(self.index == "Hyper Potion"):
                btn_info = ["item", item_objects.hyper_potion]
            elif(self.index == "Max Potion"):
                btn_info = ["item", item_objects.max_potion]
            action1, action2, action_list = battle(self.player, self.enemy, btn_info)
            self.state.set_action_list(action_list)
            print("using " + self.index)
            self.state.set_state(State.Wait)
            self.state.set_rendered(False)
            # Return to the wait view


    def on_draw(self):
        # Clear the screen
        self.clear()
        arcade.draw_lrwh_rectangle_textured(0, 0,
                                                        SCREEN_WIDTH, SCREEN_HEIGHT,
                                                        self.background_sky)
        # Draw all the sprites.
        self.manager.draw()
        self.player_list.draw()