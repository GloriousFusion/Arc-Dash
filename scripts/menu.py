from scripts.autoload.constant import *
from scripts.autoload.setting import *

from scripts.scene import Scene

class Menu:
    def __init__(self, commands, surface, xui_assets):
        self.commands = commands

        self.surface = surface
        self.scene = Scene(self.surface)

        self.xui_assets = xui_assets

    def events(self, event):
        pass # Custom menu events

    def update(self, delta):
        self.scene.update(delta)

    def render(self):
        self.scene.render()
        pygame.display.update()

class Main(Menu):
    def __init__(self, commands, surface, xui_assets):
        super().__init__(commands, surface, xui_assets)

        #   Next menu
        self.next_menu = lambda: self.commands["set_menu"]("play")

        #   Ui (xui)
        self.ui = self.scene.add_ui("ui", self.surface, self.xui_assets["font-future-millennium"])

        #   Ui elements (xui)
        self.main_logo = self.ui.add_image(
            (DISPLAY_WIDTH / 2, DISPLAY_HEIGHT / 3), self.xui_assets["logo-01"])
        self.button_play = self.ui.add_button(
            (DISPLAY_WIDTH / 2, DISPLAY_HEIGHT / 1.75), (120, 40), MENU_MAIN_BUTTON_COLOR, self.next_menu, "Start")

    def events(self, event):
        buttons = [element for element in self.ui.elements if element["type"] == "button"]
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for button in buttons:
                if button["object"].get_hover(pygame.mouse.get_pos()):
                    #   Hover: button["object"].set_hover()
                    if button["object"]:
                        button["object"].set_click()

    def render(self):
        self.scene.add_gradient(MENU_MAIN_TOP, MENU_MAIN_BOT, MENU_MAIN_BAND)
        super().render()

class Play(Menu):
    def __init__(self, commands, surface, xui_assets, assets, maps):
        super().__init__(commands, surface, xui_assets)
        self.assets = assets
        self.maps = maps

        #   Next menu
        self.next_menu = lambda: self.commands["set_menu"]("main")
        self.next_menu_trigger = False

        self.timers = {"win_time": self.scene.add_timer("timer", MENU_PLAY_WIN_TIME, self.next_menu)}

        #   Hud (xui)
        self.hud = self.scene.add_hud("hud", self.surface, self.xui_assets["font-groovy-fast"])

        #   Map (picked)
        self.map = self.scene.add_map(self.maps[SCENE_MAP])

        #   Entities (players)
        self.player1 = self.scene.add_entity(
            "player",
            PLAYER1_NAME,
            PLAYER1_CONTROLS,
            {"character_name": PLAYER1_CHARACTER, "character_texture": self.assets[f"{PLAYER1_CHARACTER}_frames"]},
            {"hand_name": f"{PLAYER1_CHARACTER}_hand", "hand_texture": self.assets[f"{PLAYER1_CHARACTER}_hand"]},
            {"weapon_name": PLAYER1_WEAPON, "weapon_texture": self.assets[PLAYER1_WEAPON],
             "projectile_name": f"{PLAYER1_WEAPON}_projectile", "projectile_texture": self.assets[f"{PLAYER1_WEAPON}_projectile"]},
            (225, -400), False)

        self.player2 = self.scene.add_entity(
            "player",
            PLAYER2_NAME,
            PLAYER2_CONTROLS,
            {"character_name": PLAYER2_CHARACTER, "character_texture": self.assets[f"{PLAYER2_CHARACTER}_frames"]},
            {"hand_name": f"{PLAYER2_CHARACTER}_hand", "hand_texture": self.assets[f"{PLAYER2_CHARACTER}_hand"]},
            {"weapon_name": PLAYER2_WEAPON, "weapon_texture": self.assets[PLAYER2_WEAPON],
             "projectile_name": f"{PLAYER2_WEAPON}_projectile", "projectile_texture": self.assets[f"{PLAYER2_WEAPON}_projectile"]},
            (725, -400), True)

    def events(self, event):
        players = [entity for entity in self.scene.entities if entity.data.type == "player"]
        if event.type == pygame.KEYDOWN:
            for player in players:
                if event.key == player.controls["use"]:
                    player.use()

    def update_win(self):
        players = [entity for entity in self.scene.entities if entity.data.type == "player"]
        for player in players:
            if player.data.winner and not self.next_menu_trigger:
                self.next_menu_trigger = True
                # self.timers["win_time"].activate()
                winner = player
                for other_player in players:
                    if other_player != winner:
                        other_player.delete()
                break

    def update_timers(self):
        for timer in self.timers.values():
            timer.update()

    def update(self, delta):
        super().update(delta)
        self.update_timers()
        self.update_win()
    
    def render(self):
        self.scene.add_gradient(MENU_PLAY_TOP, MENU_PLAY_BOT, MENU_PLAY_BAND)
        super().render()