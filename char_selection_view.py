import arcade

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
        # Determine color based on button state
        if self.is_pressed:
            color = arcade.color.BLUE
        elif self.is_hovered:
            color = arcade.color.LIGHT_GRAY
        else:
            color = arcade.color.DARK_GRAY

        # Draw button rectangle and text
        arcade.draw_rectangle_filled(self.x, self.y, self.width, self.height, color)
        arcade.draw_text(self.text, self.x, self.y, arcade.color.WHITE, font_size=20, anchor_x="center", anchor_y="center")

    def check_collision(self, x, y):
        # Check if given coordinates are inside the button area
        if self.x - self.width / 2 < x < self.x + self.width / 2 and self.y - self.height / 2 < y < self.y + self.height / 2:
            return True
        return False

class PlayerSelectView(arcade.View):
    def __init__(self):
        super().__init__()
        self.selected_player = None
        self.buttons = []
        self.character_sprites = arcade.SpriteList()

        # List of player names
        player_names = ["Billy Bob", "John Doe"]

        # Load Pokémon-like sprites
        self.character_sprites.append(arcade.Sprite(":resources:images/animated_characters/female_adventurer/femaleAdventurer_idle.png", scale=2, center_x=SCREEN_WIDTH / 4, center_y=SCREEN_HEIGHT / 4 * 2 + 40))
        self.character_sprites.append(arcade.Sprite(":resources:images/animated_characters/female_adventurer/femaleAdventurer_idle.png", scale=2, center_x=SCREEN_WIDTH * 3 / 4, center_y=SCREEN_HEIGHT / 4 * 2 + 40))

        # Load and play background music
        self.background_music = arcade.load_sound(":resources:music/funkyrobot.mp3")
        self.background_music_player = None

        # Create buttons below players
        for i in range(2):
            button = Button(player_names[i], SCREEN_WIDTH / 4 + i * SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4 - BUTTON_HEIGHT / 2 - 10, BUTTON_WIDTH, BUTTON_HEIGHT)
            self.buttons.append(button)

    def on_show(self):
        # Set background color and start background music
        arcade.set_background_color(arcade.color.LIGHT_BLUE)
        if self.background_music_player is None:
            self.background_music_player = arcade.play_sound(self.background_music, volume=0.5)

    def on_draw(self):
        # Draw everything on the screen
        arcade.start_render()

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
                game_view = GameView(player=self.selected_player)
                self.window.show_view(game_view)
                if self.background_music_player is not None:
                    arcade.stop_sound(self.background_music_player)
                break
            btn.is_pressed = False

class GameView(arcade.View):
    def __init__(self, player):
        super().__init__()
        self.player = player

        # Load and play game music
        self.game_music = arcade.load_sound(":resources:music/1918.mp3")
        self.game_music_player = None

    def on_show(self):
        # Set background color and start game music
        arcade.set_background_color(arcade.color.BLACK)
        if self.game_music_player is None:
            self.game_music_player = arcade.play_sound(self.game_music, volume=0.5)

    def on_draw(self):
        # Draw everything on the screen
        arcade.start_render()
        arcade.draw_text(f"Game Screen for {self.player}", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, arcade.color.WHITE, font_size=30, anchor_x="center")

def main():
    # Set up the window and start the application
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, "Player Select Screen")
    player_select_view = PlayerSelectView()
    window.show_view(player_select_view)
    arcade.run()

if __name__ == "__main__":
    main()