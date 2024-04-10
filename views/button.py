import arcade
import arcade.gui
from arcade.gui import UIManager

class CustomButton(arcade.gui.UIFlatButton):
    def __init__(self, text, width, style, id):
        super().__init__(text=text, width=width, style=style)
        self.id = id
    def on_click(self, event: arcade.gui.UIOnClickEvent, id):
        super().on_click(event)
        print(id)