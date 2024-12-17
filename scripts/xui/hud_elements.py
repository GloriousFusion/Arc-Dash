from scripts.autoload.constant import *
from scripts.shader.shaders import Outline

class Nametag(pygame.sprite.Sprite):
    def __init__(self, data, image, scale=0.6):
        pygame.sprite.Sprite.__init__(self)

        self.data = data

        self.scale = scale

        self.image = image
        self.image = pygame.transform.scale(self.image, ((self.image.get_width() * self.scale), (self.image.get_height() * self.scale)))

        self.shader = Outline(self.image, HUD_OUTLINE_COLOR)
        self.image = self.shader.get_output()

        self.rect = self.image.get_rect()

    def update(self, delta):
        self.rect.center = (self.data.position[0] + 10, self.data.position[1] - 10)