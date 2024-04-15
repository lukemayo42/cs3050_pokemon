import arcade
import arcade.gui
from arcade.gui import UIManager

class Button:
    def __init__(self, text, x, y, width, height, id, type):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.is_hovered = False
        self.is_pressed = False
        self.id = id
        self.type = type

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
    
