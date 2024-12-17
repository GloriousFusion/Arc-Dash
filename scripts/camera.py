from scripts.autoload.constant import *

class Camera(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.offset = Vector2(0, 0)
        self.half_w = DISPLAY_WIDTH / 2
        self.half_h = DISPLAY_HEIGHT / 2

        self.zoom = 1.25
        self.min_zoom = 1
        self.max_zoom = 1.75

        self.last_positions = {}

    def adjust(self, players):

        #   One player only (Set zoom = 2 and offset = center of screen)
        if len(players) < 2:
            if players:
                self.offset.x = -players[0].rect.centerx + self.half_w
                self.offset.y = -players[0].rect.centery + self.half_h
            self.zoom = 2
            return

        #   Fix shake (due to constant idle animation rect update)
        significant_movement = False

        for player in players:
            current_position = Vector2(player.rect.center)
            last_position = self.last_positions.get(player)

            if last_position is None:
                self.last_positions[player] = current_position
                continue

            if (current_position - last_position).length() > 1:
                self.last_positions[player] = current_position.copy()
                significant_movement = True

        if not significant_movement:
            return

        #   Zoom and offset adjustment logic
        min_x = min(player.rect.centerx for player in players)
        max_x = max(player.rect.centerx for player in players)

        min_y = min(player.rect.centery for player in players)
        max_y = max(player.rect.centery for player in players)

        player_distance_x = max_x - min_x
        player_distance_y = max_y - min_y

        max_distance = max(player_distance_x / DISPLAY_WIDTH, player_distance_y / DISPLAY_HEIGHT)
        self.zoom = max(self.min_zoom, min(self.max_zoom, 1 / (max_distance + 0.1)))

        center_x = (min_x + max_x) / 2
        center_y = (min_y + max_y) / 2
        self.offset.x = -center_x + self.half_w
        self.offset.y = -center_y + self.half_h

    def draw(self, surface, entities):
        players = [entity for entity in entities if entity.data.type == "player"]
        self.adjust(players)

        #   Zoom and offset drawing logic
        render_surface = pygame.Surface((DISPLAY_WIDTH, DISPLAY_HEIGHT), pygame.SRCALPHA)

        for sprite in self:
            offset = sprite.rect.topleft + self.offset
            render_surface.blit(sprite.image, offset)

        scaled_surface = pygame.transform.scale(render_surface,
                                                (int(DISPLAY_WIDTH * self.zoom),
                                                 int(DISPLAY_HEIGHT * self.zoom)))

        surface.blit(scaled_surface,
                     ((DISPLAY_WIDTH - scaled_surface.get_width()) // 2,
                      (DISPLAY_HEIGHT - scaled_surface.get_height()) // 2))