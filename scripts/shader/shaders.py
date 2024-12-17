from scripts.autoload.constant import *

class Shader:
    def __init__(self, image):
        self.image = image
        self.mask = pygame.mask.from_surface(self.image)

        self.output = self.image

    def get_output(self):
        return self.output

class Color(Shader):
    def __init__(self, image, color):
        super().__init__(image)
        self.color = color

        self.output = pygame.Surface(self.image.get_size(), pygame.SRCALPHA)

        for y in range(self.mask.get_size()[1]):
            for x in range(self.mask.get_size()[0]):
                if self.mask.get_at((x, y)):
                    self.output.set_at((x, y), self.color)
                else:
                    self.output.set_at((x, y), BLACK)

class Outline(Shader):
   def __init__(self, image, color, thickness=1):
       super().__init__(image)
       self.color = color
       self.thickness = thickness

       self.output = pygame.Surface(
           (self.image.get_width() + self.thickness * 2,
            self.image.get_height() + self.thickness * 2),
           pygame.SRCALPHA
       )

       for x in range(-self.thickness, self.thickness + 1):
           for y in range(-self.thickness, self.thickness + 1):
               if x != 0 or y != 0:
                   self.output.blit(
                       self.mask.to_surface(setcolor=self.color, unsetcolor=BLACK),
                       (x + self.thickness, y + self.thickness)
                   )

       self.output.blit(self.image, (self.thickness, self.thickness))