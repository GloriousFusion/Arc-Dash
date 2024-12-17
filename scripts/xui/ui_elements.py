from scripts.autoload.constant import *

class Button:
    def __init__(self, position, dimension, color, on_click):

        self.position = position
        self.dimension = dimension
        self.color = color

        self.rect = pygame.Rect(position[0] - dimension[0] / 2, position[1] - dimension[1] / 2, *dimension)

        self.on_click = on_click

    def get_surface(self):
        surface = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        pygame.draw.rect(surface, self.color, surface.get_rect())
        return surface

    def get_hover(self, position):
        return self.rect.collidepoint(position)

    def set_click(self):
        self.on_click()

class TextButton(Button):
    def __init__(self, position, dimension, color, text=None, on_click=None):
        super().__init__(position, dimension, color, on_click)
        self.text = text

    def get_surface(self):
        surface = super().get_surface()

        text_rect = self.text.get_rect(center=(self.rect.width / 2, self.rect.height / 2))
        surface.blit(self.text, text_rect)
        return surface