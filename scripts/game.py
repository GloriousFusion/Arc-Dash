from scripts.autoload.constant import *
from scripts.autoload.utility import *

from scripts.menu import Main, Play

class Game:
    def __init__(self):
        pygame.init()

        #   Screen
        self.display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT), DISPLAY_FLAGS)
        pygame.display.set_caption(DISPLAY_TITLE)

        #   Time
        self.clock = pygame.time.Clock()
        self.delta = 0

        #   Assets
        self.assets = {
            #   Character (Frames)
            "biker_frames": import_sub_folders("..", "assets", "characters", "biker", "frames"),
            "punk_frames": import_sub_folders("..", "assets", "characters", "punk", "frames"),
            "cyborg_frames": import_sub_folders("..", "assets", "characters", "cyborg", "frames"),
            #   Character (Hand)
            "biker_hand": import_folder("..", "assets", "characters", "biker", "hand"),
            "punk_hand": import_folder("..", "assets", "characters", "punk", "hand"),
            "cyborg_hand": import_folder("..", "assets", "characters", "cyborg", "hand"),
            #   Weapon (Pistol)
            "pulse_blaster": import_image("..", "assets", "weapons", "pistol", "pulse_blaster"),
            "ion_dart": import_image("..", "assets", "weapons", "pistol", "ion_dart"),
            "electro_bolter": import_image("..", "assets", "weapons", "pistol", "electro_bolter"),
            #   Projectile (Bullet)
            "pulse_blaster_projectile": import_image("..", "assets", "projectiles", "bullet", "pulse_blaster"),
            "ion_dart_projectile": import_image("..", "assets", "projectiles", "bullet", "ion_dart"),
            "electro_bolter_projectile": import_image("..", "assets", "projectiles", "bullet", "electro_bolter"),
        }

        self.xui_assets = {
            #   Ui (Logos)
            "logo-01": import_image("..", "assets", "xui", "logos", "logo-01"),
            #   Ui (Fonts)
            "font-future-millennium": import_font("..", "assets", "xui", "fonts", "future-millennium", font_size=24),
            #   Hud (Fonts)
            "font-groovy-fast": import_font("..", "assets", "xui", "fonts", "groovy-fast", font_size=16)
        }

        #   Maps
        self.maps = {
            0: import_map("..", "assets", "maps", "park_zone", "park_zone.tmx")
        }

        #   Commands
        self.commands = {
            "set_menu": self.set_menu
        }

        ### Menus ###
        #   Main
        self.menu_main = Main(self.commands, self.display, self.xui_assets)
        #   Play
        self.menu_play = Play(self.commands, self.display, self.xui_assets, self.assets, self.maps)

        #   All Menus
        self.menus = {
            "main": self.menu_main,
            "play": self.menu_play
        }

        #   Current Menu
        self.menu = self.menus["main"]

        self.running = True

    def set_menu(self, menu):
        self.menu = self.menus[menu]

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.running:
                    self.running = False
            self.menu.events(event)

    def update(self):
        self.menu.update(self.delta)

    def render(self):
        self.menu.render()

    def run(self):
        while self.running:
            self.delta = self.clock.tick(60) * 0.001

            self.events()
            self.update()
            self.render()

if __name__ == "__main__":
    game = Game()
    game.run()