from scripts.autoload.constant import *

class Debug(pygame.sprite.Sprite):
    def __init__(self, rect, position=(0, 0), color=WHITE, func=None):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface(rect)
        self.image.fill(color)

        self.rect = pygame.Rect(position, rect)

        self.func = func

    def set_function(self, func, *data):
        self.func = func
        self.func(*data)

    def set_position(self, rect_position):
        self.rect.topleft = rect_position