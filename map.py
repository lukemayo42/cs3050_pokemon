"""
Move with a Sprite Animation

Simple program to show basic sprite usage.

Artwork from https://kenney.nl

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.sprite_move_animation
"""
import arcade
import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Move with a Sprite Animation Example"

CHARACTER_SCALING = 0.5


# How fast to move, and how fast to run the animation

MOVEMENT_SPEED = 1.5

UPDATES_PER_FRAME = 5



# Constants used to track if the player is facing left or right

RIGHT_FACING = 0

LEFT_FACING = 1




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

        self.character_face_direction = RIGHT_FACING

        # Used for flipping between image sequences

        self.cur_texture = 0

        self.scale = CHARACTER_SCALING

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

        if self.change_x < 0 and self.character_face_direction == RIGHT_FACING:

            self.character_face_direction = LEFT_FACING

        elif self.change_x > 0 and self.character_face_direction == LEFT_FACING:

            self.character_face_direction = RIGHT_FACING



        # Idle animation

        if self.change_x == 0 and self.change_y == 0:

            self.texture = self.idle_texture_pair[self.character_face_direction]

            return



        # Walking animation

        self.cur_texture += 1

        if self.cur_texture > 7 * UPDATES_PER_FRAME:

            self.cur_texture = 0

        frame = self.cur_texture // UPDATES_PER_FRAME

        direction = self.character_face_direction

        self.texture = self.walk_textures[frame][direction]


class WorldMap(arcade.Window):
    """ Main application class. """

    def __init__(self, width, height, title):
        """ Set up the game and initialize the variables. """
        super().__init__(width, height, title)

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
                                 CHARACTER_SCALING)
            wall.center_x = x
            wall.center_y = 0
            self.wall_list.append(wall)

        # Create a row of boxes
        for x in range(400, 600, 64):
            wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png",
                                 CHARACTER_SCALING)
            wall.center_x = x
            wall.center_y = 580
            self.wall_list.append(wall)

        # Create a row of boxes
        for x in range(80, 350, 64):
            wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png",
                                 CHARACTER_SCALING)
            wall.center_x = x
            wall.center_y = 520
            self.wall_list.append(wall)

        # Create a row of boxes
        for x in range(500, 580, 24):
            wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png",
                                 CHARACTER_SCALING-0.3)
            wall.center_x = x
            wall.center_y = 240
            self.wall_list.append(wall)

        # Create a row of boxes
        for x in range(330, 520, 64):
            wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png",
                                 CHARACTER_SCALING + 0.2)
            wall.center_x = x
            wall.center_y = 120
            self.wall_list.append(wall)

        wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png",
                             CHARACTER_SCALING + 0.7)
        wall.center_x = 220
        wall.center_y = 340
        self.wall_list.append(wall)

        wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png",
                             CHARACTER_SCALING + 0.2)
        wall.center_x = 460
        wall.center_y = 430
        self.wall_list.append(wall)

        wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png",
                             CHARACTER_SCALING + 0.2)
        wall.center_x = 420
        wall.center_y = 280
        self.wall_list.append(wall)

        wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png",
                             CHARACTER_SCALING - 0.2)
        wall.center_x = 305
        wall.center_y = 185
        self.wall_list.append(wall)

        # Create a column of boxes
        for y in range(250, 380, 34):
            wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png",
                                 CHARACTER_SCALING - 0.2)
            wall.center_x = 490
            wall.center_y = y
            self.wall_list.append(wall)

        # Create a column of boxes
        for y in range(310, 430, 64):
            wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png",
                                 CHARACTER_SCALING+0.2)
            wall.center_x = 310
            wall.center_y = y
            self.wall_list.append(wall)

        # Create a column of boxes
        for y in range(0, 700, 64):
            wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png",
                                 CHARACTER_SCALING)
            wall.center_x = 50
            wall.center_y = y
            self.wall_list.append(wall)

        # Create a column of boxes
        for y in range(0, 700, 64):
            wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png",
                                 CHARACTER_SCALING)
            wall.center_x = 600
            wall.center_y = y
            self.wall_list.append(wall)

        # Create a column of boxes
        for y in range(120, 220, 54):
            wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png",
                                 CHARACTER_SCALING+0.1)
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
            self.player.change_y = MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            self.player.change_y = -MOVEMENT_SPEED
        elif key == arcade.key.LEFT:
            self.player.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player.change_x = MOVEMENT_SPEED

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


def main():
    """ Main function """
    window = WorldMap(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()