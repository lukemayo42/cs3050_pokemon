import arcade
from state import State
from Character import Character

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 40

class Button:
    def __init__(self, text, x, y, width, height):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.is_hovered = False
        self.is_pressed = False

    def draw(self):
        # Set the color and border color of buttons
        color = (50, 75, 125)
        border_color = arcade.color.WHITE

        # Draw button rectangle and text
        arcade.draw_rectangle_filled(self.x, self.y, self.width, self.height, color)

        # Draw button rectangle outline (border)
        if self.is_hovered or self.is_pressed:
            arcade.draw_rectangle_outline(self.x, self.y, self.width, self.height, border_color, border_width=3)

        arcade.draw_text(self.text, self.x, self.y, arcade.color.WHITE, font_size=20, anchor_x="center", anchor_y="center")

    def check_collision(self, x, y):
        # Check if given coordinates are inside the button area
        if self.x - self.width / 2 < x < self.x + self.width / 2 and self.y - self.height / 2 < y < self.y + self.height / 2:
            return True
        return False

class PlayerSelectView(arcade.View):
    def __init__(self, player, state):
        super().__init__()
        self.state = state
        self.player = player
        self.selected_player = None
        self.buttons = []
        self.character_sprites = arcade.SpriteList()

        # List of player names
        player_names = ["Ace Darkstar", "Nova Blaze"]

        # Load Pokémon-like sprites
        self.character_sprites.append(arcade.Sprite(":resources:images/animated_characters/male_person/malePerson_idle.png", scale=2, center_x=SCREEN_WIDTH / 4, center_y=SCREEN_HEIGHT / 4 * 2 + 40))
        self.character_sprites.append(arcade.Sprite(":resources:images/animated_characters/female_adventurer/femaleAdventurer_idle.png", scale=2, center_x=SCREEN_WIDTH * 3 / 4, center_y=SCREEN_HEIGHT / 4 * 2 + 40))

        # Create buttons below players
        for i in range(2):
            button = Button(player_names[i], SCREEN_WIDTH / 4 + i * SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4 - BUTTON_HEIGHT / 2 - 10, BUTTON_WIDTH, BUTTON_HEIGHT)
            self.buttons.append(button)

    def on_show(self):
        # Set background color and start background music
        arcade.set_background_color(arcade.color.LIGHT_BLUE)
       
    def on_draw(self):
        # Draw everything on the screen
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0, 0,
                                        SCREEN_WIDTH, SCREEN_HEIGHT,
                                        arcade.load_texture("../cs3050_pokemon/images/screen_background.png"))
        # Draw title text
        arcade.draw_text("Select Your Player", SCREEN_WIDTH / 2, SCREEN_HEIGHT - 50, arcade.color.WHITE, font_size=30, anchor_x="center")

        # Draw character sprites
        self.character_sprites.draw()


        # Draw buttons
        for button in self.buttons:
            button.draw()

    def on_mouse_motion(self, x, y, dx, dy):
        # Handle mouse motion events
        for button in self.buttons:
            if button.check_collision(x, y):
                button.is_hovered = True
            else:
                button.is_hovered = False

    def on_mouse_press(self, x, y, button, modifiers):
        # Handle mouse press events
        for button in self.buttons:
            if button.check_collision(x, y):
                button.is_pressed = True
            else:
                button.is_pressed = False

    def on_mouse_release(self, x, y, button, modifiers):
        # Handle mouse release events
        for btn in self.buttons:
            if btn.is_pressed and btn.check_collision(x, y):
                self.selected_player = btn.text
                if (self.selected_player == "Ace Darkstar"):
                    self.state.set_character_sprite(":resources:images/animated_characters/male_person/malePerson_idle.png")
                    self.player.set_name("Ace Darkstar")
                else:
                    self.state.set_character_sprite(
                        ":resources:images/animated_characters/female_adventurer/femaleAdventurer_idle.png")
                    self.player.set_name("Nova Blaze")

                if (self.state.get_state().value == State.CharacterSelect.value):
                    self.state.set_state(State.Party)
                    self.state.set_rendered(False)

                break
            btn.is_pressed = False