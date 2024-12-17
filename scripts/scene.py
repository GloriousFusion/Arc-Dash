from scripts.autoload.constant import *

from scripts.camera import Camera

from scripts.xui.ui import Ui
from scripts.xui.hud import Hud
from scripts.xui.hud_elements import Nametag

from scripts.object.debuggers import Debug
from scripts.object.timers import Timer
from scripts.object.objects import Tile, Hand, Pistol, Bullet

from scripts.entity.player import Player

class Scene:
    def __init__(self, surface):
        self.surface = surface

        self.camera = Camera()

        self.ui = None
        self.hud = None

        self.hud_elements = pygame.sprite.Group()

        self.objects = pygame.sprite.Group()
        self.entities = pygame.sprite.Group()

        self.collisions = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()

        self.groups = {
            "camera": self.camera, "hud_elements": self.hud_elements,
            "objects": self.objects, "entities": self.entities,
            "collisions": self.collisions, "projectiles": self.projectiles
        }

        self.xui_ui = {
            "ui": Ui
        }

        self.xui_hud = {
            "hud": Hud
        }

        self.xui_hud_elements = {
            "nametag": Nametag
        }

        self.object_debuggers = {
            "debug": Debug
        }

        self.object_timers = {
            "timer": Timer
        }

        self.object_objects = {
            "tile": Tile,
            "hand": Hand,
            "pistol": Pistol,
            "bullet": Bullet
        }

        self.entity_entities = {
            "player": Player
        }

        self.commands = {
            "add_hud_element": self.add_hud_element,
            "add_debugger": self.add_debugger,
            "add_timer": self.add_timer,
            "add_object": self.add_object,
            "remove_object": self.remove_object,
            "get_hud_elements": self.get_hud_elements,
            "get_entities": self.get_entities,
            "get_collisions": self.get_collisions,
            "debug": self.debug
        }

    def add_color(self, color=WHITE):
        self.surface.fill(color)

    def add_gradient(self, top_color, bottom_color, band_height):
        for y in range(0, DISPLAY_HEIGHT, band_height):
            gradient = top_color.lerp(bottom_color, y / DISPLAY_HEIGHT)
            self.surface.fill(gradient, (0, y, DISPLAY_WIDTH, band_height))

    def add_ui(self, ui_type, *data):
        self.ui = self.xui_ui[ui_type](self.commands, *data)
        return self.ui

    def add_hud(self, hud_type, *data):
        self.hud = self.xui_hud[hud_type](self.commands, *data)
        return self.hud

    def add_hud_element(self, element_type, *data):
        element = self.xui_hud_elements[element_type](*data)
        self.groups["camera"].add(element)
        self.groups["hud_elements"].add(element)
        return element

    def add_map(self, map_id):

        #   Tiles (Platforms: Collision)
        for layer in ["platform"]:
            for x, y, image in map_id.get_layer_by_name(layer).tiles():
                tile = self.object_objects["tile"](self.commands, "tile", image, (x * TILE_SIZE, y * TILE_SIZE), TILE_TOLERANCE)
                self.groups["camera"].add(tile)
                self.groups["collisions"].add(tile)

        #
        #   Tiles (Objects: Collision)
        #
        #   Tiles (Objects: Interactable)
        #

        #   Tiles (Objects: Background)
        for layer in ["background_layer2", "background_layer1"]:
            for obj in map_id.get_layer_by_name(layer):
                background_tile = self.object_objects["tile"](self.commands, "tile", obj.image, (obj.x, obj.y), TILE_TOLERANCE)
                self.groups["camera"].add(background_tile)

    def add_entity(self, entity_type, *data, group=None):
        entity = self.entity_entities[entity_type](self.commands, self.hud, *data)
        self.groups["camera"].add(entity)
        self.groups["entities"].add(entity)

        if group:
            self.groups[group].add(entity)

        return entity

    def add_object(self, object_type, *data, group=None):
        obj = self.object_objects[object_type](self.commands, *data)
        self.groups["camera"].add(obj)
        self.groups["objects"].add(obj)

        if group:
            self.groups[group].add(obj)

        return obj

    def add_timer(self, object_type, *data):
        timer = self.object_timers[object_type](*data)
        return timer

    def add_debugger(self, object_type, *data):
        debugger = self.object_debuggers[object_type](*data)
        self.groups["camera"].add(debugger)
        return debugger

    def remove_object(self, obj, group):
        self.groups[group].remove(obj)

    def get_hud_elements(self):
        return self.hud_elements

    def get_collisions(self):
        return self.collisions

    def get_entities(self):
        return self.entities

    def update(self, delta):
        self.camera.update(delta)

    def render(self):
        self.camera.draw(self.surface, self.entities)

        if self.ui:
            self.ui.render()

        if self.hud:
            self.hud.render()

    @staticmethod
    def debug(obj, func, *data):
        obj.set_function(func, *data)