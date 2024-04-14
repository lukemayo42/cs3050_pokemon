import arcade
import arcade.gui
import math

# Constants for health bar sprites
HEALTH_BAR_SCALAR = 125
HEALTH_BAR_BORDER = 12
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

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

# This HealthBar class is a subclass of the Sprite arcade class that displays the health and name
# of pokemon on the screen in text sprites. It has a health_bar_update method that rewrites the sprite.
class HealthBar(arcade.Sprite):
    def __init__(self, pokemon, sprite_list, pos_x, pos_y, name_pos, is_current):
        super().__init__()
        self.pokemon = pokemon
        self.is_current = is_current
        #self.health = health
        
        if self.is_current:
            self.health = pokemon.get_curr_hlth()
            print(f"current: {self.health}")
        else:
            self.health = pokemon.get_prev_hlth()
            print(f"previous:{self.health}")
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

    #we need a method that will update only one of the health bars at a time