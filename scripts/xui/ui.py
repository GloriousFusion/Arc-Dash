from scripts.autoload.constant import *

from scripts.xui.ui_elements import TextButton

class Ui:
    def __init__(self, commands, surface, font):
        self.commands = commands

        self.surface = surface
        self.font = font

        self.elements = []

    def add_image(self, position, image):
        rect = image.get_rect(center=position)
        self.elements.append({"type": "image", "data": image, "rect": rect})

    def add_button(self, position, dimension, color, on_click=None, text=None, text_color=WHITE):
        button_text = self.font.render(text, False, text_color)
        button = TextButton(position, dimension, color, button_text, on_click)
        self.elements.append({"type": "button", "object": button, "data": button.get_surface(), "rect": button.rect})

    def render(self):
        for element in self.elements:
            self.surface.blit(element["data"], element["rect"])