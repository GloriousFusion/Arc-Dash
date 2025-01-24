from scripts.autoload.constant import *
from scripts.autoload.variable import EntityData

from scripts.shader.shaders import Color, Outline

class Player(pygame.sprite.Sprite):
    def __init__(self, commands=None, hud=None, name=None, controls=None, player=None, hand=None, weapon=None, position=(0, 0), flip=False, scale=1):
        pygame.sprite.Sprite.__init__(self)

        #   Inherited objects (under hierarchy of player)
        self.objects = pygame.sprite.Group()

        #   Dictionary of commands (functions from scene)
        self.commands = commands

        #   Key controls
        self.controls = controls

        #   Declare variable data
        self.data = EntityData(hud, name, "player", "idle", position)

        #   Texture (animations and state)
        self.character_name = player["character_name"]
        self.frames, self.index = player["character_texture"], 0
        self.flip = flip
        self.image = self.frames[self.data.state][self.index]

        #   Apply scale and position
        self.scale = scale

        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * self.scale), int(self.image.get_height() * self.scale)))
        self.rect = self.image.get_frect(topleft=self.data.position)

        #   Declare rects (hurtbox)
        self.hurtbox = self.set_hurtbox()

        #   Declare velocity, acceleration and knockback (movement vectors)
        self.velocity = Vector2(0, 0)
        self.acceleration = Vector2(0, 0)
        self.knockback = Vector2(0, 0)

        #   Declare jump amount (allows for double or triple jumping)
        self.jump_amount = ENTITY_JUMP_AMOUNT

        #   Declare collision handling (list of collisions and collision mask)
        self.collisions = self.commands["get_collisions"]()
        self.mask = None

        #   Declare targets (other entities, in order to get the nearest one)
        self.targets = self.commands["get_entities"]()

        self.nearest_target = None
        self.min_distance = float("inf")

        #   Declare weapon and hand (and add weapon to hand)
        self.weapon = self.commands["add_object"](
            "pistol", weapon["weapon_name"], weapon["weapon_texture"],
            {"name": weapon["projectile_name"], "texture": weapon["projectile_texture"]})
        self.hand = self.commands["add_object"]("hand", hand["hand_name"], hand["hand_texture"], self.weapon)


        #   Declare timers
        self.timers = {
            "platform_skip": self.commands["add_timer"]("timer", ENTITY_SKIP_TIME),
            "hurt_time": self.commands["add_timer"]("timer", ENTITY_HURT_TIME),
            "respawn_time": self.commands["add_timer"]("timer", PLAYER_RESPAWN_TIME)
        }

        ### States ###
        #   On floor (on top of platform/collider)
        self.on_floor = False
        #   On move (moving right or left)
        self.on_move = False
        #   On jump (jumping up)
        self.on_jump = False
        #   On skip (dropping down from platform)
        self.on_skip = False
        #   On hurt (collided with object that hurts)
        self.on_hurt = False
        #   On death (dead rip)
        self.on_death = False

        #   Add objects to inherited hierarchy
        self.objects.add(self.weapon, self.hand)

        ### Debug ###
        if DEBUG:
            self.debug_hurtbox = self.commands["add_debugger"]("debug", (self.hurtbox.width, self.hurtbox.height), (self.hurtbox.x, self.hurtbox.y), WHITE)

    def input(self):
        keys = pygame.key.get_pressed()

        if not self.on_move and not self.on_jump:
            self.data.state = "idle"
            self.acceleration.x = 0

        if keys[self.controls["right"]]:
            self.data.state = "run"
            self.acceleration.x = ENTITY_ACCELERATION
            self.flip = False
        if keys[self.controls["left"]]:
            self.data.state = "run"
            self.acceleration.x = -ENTITY_ACCELERATION
            self.flip = True

        if keys[self.controls["right"]] or keys[self.controls["left"]]:
            self.on_move = True
        if not keys[self.controls["right"]] or keys[self.controls["left"]]:
            self.on_move = False

        if keys[self.controls["up"]] and not self.on_jump:
            if self.jump_amount > 0:
                self.jump()
        if not keys[self.controls["up"]]:
            self.on_jump = False

        if keys[self.controls["down"]]:
            self.skip()
        if not self.timers["platform_skip"].active:
            self.on_skip = False

    def move(self, delta):
        self.acceleration.y = ENTITY_GRAVITY if not self.on_floor else 0

        self.acceleration.x += self.velocity.x * -ENTITY_FRICTION
        self.velocity += self.acceleration + self.knockback

        self.data.position += self.velocity + ENTITY_ACCELERATION * self.acceleration * delta
        self.rect.topleft = self.data.position

        self.knockback *= ENTITY_FRICTION

        self.check()
        self.target()
        self.death()

    def jump(self):
        self.velocity.y = -ENTITY_JUMP_FORCE
        self.jump_amount -= 1
        self.on_jump = True

    def skip(self):
        self.acceleration.y = ENTITY_SKIP_FORCE
        self.on_skip = True
        self.timers["platform_skip"].activate()

    def use(self):
        # Update hand/weapon based on desired weapon action
        if self.data.state != "death":
            self.hand.set_action()

    def hurt(self, knockback):
        self.knockback = knockback
        self.on_hurt = True
        self.timers["hurt_time"].activate()

    def death(self):
        if self.rect.y > DISPLAY_HEIGHT:
            if self.nearest_target:
                if self.nearest_target.data.type == "player":
                    if not self.on_death and not self.data.winner:
                        self.nearest_target.data.score += 1
                        self.on_death = True
                        self.timers["respawn_time"].activate()

                    if not self.timers["respawn_time"].active:
                        self.velocity = Vector2(0, 0)
                        self.data.position = PLAYER_RESPAWN_POSITION
                        self.on_death = False

    def animate(self, delta):
        self.index += ANIMATION_SPEED * delta
        self.image = self.frames[self.data.state][int(self.index % len(self.frames[self.data.state]))]
        self.image = pygame.transform.flip(self.image, self.flip, False)

        #   Update rect (consistency with collision check)
        if self.flip:
            self.set_rect("topleft")

        #   Update hand (flip direction and position)
        self.hand.flip = self.flip
        self.hand.set_position(self.rect, HAND_OFFSET[self.hand.name])

        #   Hurt animation (color shader + outline shader effect)
        if self.timers["hurt_time"].active:
            shader = Color(self.image, ENTITY_HURT_COLOR)
            self.image = shader.get_output()

            shader = Outline(self.image, ENTITY_HURT_OUTLINE_COLOR)
            self.image = shader.get_output()

    def check(self):
        self.on_floor = False

        #   Update mask and rect (consistency with animation frame)
        if not self.flip:
            self.set_rect("topright")

        self.mask = pygame.mask.from_surface(self.image)

        for collider in self.collisions:

            if self.on_skip:
                continue

            if pygame.sprite.collide_mask(self, collider):
                if self.velocity.y > 0:
                    if self.rect.bottom <= collider.rect.top + self.velocity.y + collider.tolerance:
                        self.rect.bottom = collider.rect.top
                        self.velocity.y = 0
                        self.on_floor = True
                        self.jump_amount = ENTITY_JUMP_AMOUNT
        self.data.position = self.rect.topleft

    def target(self):
        for target in self.targets:

            if target == self:
                continue

            distance = abs(self.rect.x - target.rect.x)
            if distance < self.min_distance:
                self.min_distance = distance
                self.nearest_target = target

        if self.nearest_target:
            self.hand.set_aim(self.rect, self.nearest_target.rect)

    def set_rect(self, orientation):
        if orientation == "topleft":
            self.rect = self.image.get_frect(topleft=self.rect.topleft)
        if orientation == "topright":
            self.rect = self.image.get_frect(topright=self.rect.topright)

        ### Update ###
        self.hurtbox = self.set_hurtbox()

        ### Debug ###
        #   Hurtbox
        if DEBUG:
            self.commands["debug"](self.debug_hurtbox, self.debug_hurtbox.set_position, (self.hurtbox.x, self.hurtbox.y))

    def set_hurtbox(self):
        return self.rect.copy().inflate(PLAYER_HURTBOX_OFFSET[self.character_name])

    def update_timers(self):
        for timer in self.timers.values():
            timer.update()

    def update(self, delta):
        self.update_timers()

        self.input()
        self.move(delta)
        self.animate(delta)

    def delete(self):
        for obj in self.objects:
            obj.kill()

        self.data.state = "death"
        self.kill()

        ### Debug ###
        if DEBUG:
            self.debug_hurtbox.kill()