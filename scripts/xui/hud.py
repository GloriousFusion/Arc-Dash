from scripts.autoload.constant import *
from scripts.shader.shaders import Outline

class Hud:
    def __init__(self, commands, surface, font):
        self.commands = commands

        self.surface = surface
        self.font = font

        self.data = []

    def add_data(self, data):
        self.data.append(data)
        self.initialize_elements(data)

    def initialize_elements(self, data):
        self.nametags(data)

    def nametags(self, data):
        name_text = self.font.render(data.name, False, HUD_NAMETAG_COLOR)
        self.commands["add_hud_element"]("nametag", data, name_text)

    def scoreboard(self):
        for idx, data in enumerate(self.data):
            name_text = self.font.render(f"{data.name}:", False, HUD_SCOREBOARD_COLOR)

            shader = Outline(name_text, HUD_OUTLINE_COLOR)
            name_text = shader.get_output()
            self.surface.blit(name_text, (20, 20 + idx * 24))

            score_text = self.font.render(str(data.score), False, HUD_SCOREBOARD_COLOR)

            shader = Outline(score_text, HUD_OUTLINE_COLOR)
            score_text = shader.get_output()
            self.surface.blit(score_text, (name_text.get_width() + 32, 20 + idx * 24))

    def win_overlay(self):
        for idx, data in enumerate(self.data):
            if data.winner:
                win_overlay = pygame.Surface((DISPLAY_WIDTH, DISPLAY_HEIGHT), pygame.SRCALPHA)
                win_overlay.set_alpha(128)
                win_overlay.fill(HUD_WIN_OVERLAY_COLOR)
                self.surface.blit(win_overlay, (0, 0))

                win_text = self.font.render("Victory Confirmed!", False, WHITE)
                self.surface.blit(win_text, (DISPLAY_WIDTH / 2 - win_text.get_width() / 2, DISPLAY_HEIGHT / 4))

    def render(self):
        self.scoreboard()
        self.win_overlay()

    def delete_elements(self, data):
        for element in self.commands["get_hud_elements"]():
            if element.data == data:
                element.kill()