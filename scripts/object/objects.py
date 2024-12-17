from scripts.autoload.constant import *

class Object(pygame.sprite.Sprite):
    def __init__(self, commands, name, image, position=(0, 0), flip=False, scale=1):
        pygame.sprite.Sprite.__init__(self)
        self.commands = commands

        self.position = position
        self.flip, self.flipped = flip, False
        self.scale = scale

        self.image = image
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * self.scale), int(self.image.get_height() * self.scale)))
        self.image = pygame.transform.flip(self.image, self.flip, False)
        self.rect = self.image.get_frect(topleft=self.position)

        self.name = name

class FrameObject(Object):
    def __init__(self, commands, name, frames):
        self.frames, self.index = frames, 0
        super().__init__(commands, name, self.frames[self.index])

        self.image = self.frames[self.index]


#   Objects (Scene)


class Tile(Object):
    def __init__(self, commands, name, image, position, tolerance):
        super().__init__(commands, name, image, position)

        self.tolerance = tolerance

        self.mask = pygame.mask.from_surface(self.image)

class Hand(FrameObject):
    def __init__(self, commands, name, frames, weapon=None):
        super().__init__(commands, name, frames)
        self.direction, self.angle = "straight", 0
        self.image = self.frames[HAND_DIRECTION[self.direction]["frame"]]

        self.weapon = weapon

    def set_position(self, rect, offset):
        if self.flip:
            self.rect.midright = (rect.midright[0] - offset[0], rect.midright[1] + offset[1])
        else:
            self.rect.midleft = (rect.midleft[0] + offset[0], rect.midleft[1] + offset[1])

        if self.flip != self.flipped:
            self.image = pygame.transform.flip(self.image, True, False)
            self.flipped = self.flip

        if self.weapon:
            self.weapon.set_position(self.rect, self.flip)

    def set_direction(self, direction):
        self.direction = direction
        self.image = self.frames[HAND_DIRECTION[self.direction]["frame"]]

    def set_angle(self, rect_y, rect_x, facing=False):
        if self.flipped:
            rect_x = -rect_x

        self.angle = math.atan2(rect_y, rect_x) if facing else 0

    def set_aim(self, shooter_rect, target_rect):
        rect_x, rect_y = target_rect.centerx - shooter_rect.centerx, target_rect.centery - shooter_rect.centery

        # Not facing target logic
        if (rect_x > 0 and self.flip) or (rect_x < 0 and not self.flip):
            self.set_direction("straight")
            self.set_angle(rect_y, rect_x, False)
            self.image = pygame.transform.flip(self.image, self.flip, False)

            if self.weapon:
                self.weapon.set_direction(self.direction)
            return

        # Is facing target logic
        distance = math.sqrt(rect_x ** 2 + rect_y ** 2)
        self.set_angle(rect_y, rect_x, True)

        base_threshold = BASE_AIM_THRESHOLD
        distance_factor = max(DISTANCE_AIM_CLOSE, distance / DISTANCE_AIM_FAR)
        threshold = base_threshold / distance_factor

        if -threshold < self.angle < threshold:
            self.set_direction("straight")
        elif threshold <= self.angle < 3 * threshold:
            self.set_direction("half_down")
        elif -3 * threshold <= self.angle < -threshold:
            self.set_direction("half_up")
        elif self.angle >= 3 * threshold:
            self.set_direction("down")
        elif self.angle <= -3 * threshold:
            self.set_direction("up")
        self.image = pygame.transform.flip(self.image, self.flip, False)

        if self.weapon:
            self.weapon.set_direction(self.direction)

    def set_action(self):
        self.weapon.set_action(self.angle)

class Pistol(Object):
    def __init__(self, commands, name, image, projectile=None):
        super().__init__(commands, name, image)
        self.direction, self.rotation = "straight", 0
        self.offset, self.muzzle = PISTOL_DIRECTION[self.name][self.direction]["offset"], PISTOL_DIRECTION[self.name][self.direction]["muzzle"]

        self.original_image = self.image

        self.projectile = projectile

    def set_position(self, rect, flip):
        self.rect = rect.copy()
        flipped_image = self.original_image

        if flip:
            self.muzzle = (-self.muzzle[0], self.muzzle[1])
            self.rect.x -= self.offset[0]
            flipped_image = pygame.transform.flip(self.original_image, True, False)
        else:
            self.muzzle = (self.muzzle[0], self.muzzle[1])
            self.rect.x += self.offset[0]

        self.rect.y += self.offset[1]

        self.image = pygame.transform.rotate(flipped_image, self.rotation)
        self.rect = self.image.get_rect(center=self.rect.center)

        self.flipped = flip

    def set_direction(self, direction):
        self.direction = direction
        self.offset = PISTOL_DIRECTION[self.name][self.direction]["offset"]
        self.muzzle = PISTOL_DIRECTION[self.name][self.direction]["muzzle"]

        self.rotation = HAND_DIRECTION[self.direction]["rotation"]
        if self.flipped:
            self.rotation = -self.rotation

    def set_action(self, angle):
        if self.projectile:
            projectile = self.commands["add_object"]("bullet", self.projectile["name"], self.projectile["texture"], group="projectiles")
            projectile_offset = (self.rect.centerx + self.muzzle[0], self.rect.centery + self.muzzle[1])
            projectile.shoot(projectile_offset, angle, self.flipped)

class Bullet(Object):
    def __init__(self, commands, name, image):
        super().__init__(commands, name, image)
        self.speed = BULLET_STATS[self.name]["speed"]
        self.force = BULLET_STATS[self.name]["force"]

        self.velocity = Vector2(0, 0)
        self.knockback = Vector2(0, 0)

        self.collisions = commands["get_entities"]()
        self.hitbox = self.set_hitbox()

        self.timers = {
            "bullet_time": self.commands["add_timer"]("timer", BULLET_TIME)
        }

        ### Debug ###
        # self.debug_hitbox = self.commands["add_debugger"]("debug", (self.hitbox.width, self.hitbox.height), (self.hitbox.x, self.hitbox.y), WHITE)

    def shoot(self, rect, angle, flipped):
        self.rect.center = rect
        
        self.velocity.x = self.speed * math.cos(angle)
        self.knockback.x = self.force * math.cos(angle)

        if flipped:
            self.velocity.y = -self.speed * math.sin(angle)
            self.velocity = -self.velocity

            self.knockback.y = -self.force * math.sin(angle)
            self.knockback = -self.knockback
        else:
            self.velocity.y = self.speed * math.sin(angle)
            self.knockback.y = self.force * math.sin(angle)

        self.timers["bullet_time"].activate()

    def move(self, delta):
        self.rect.x += self.velocity.x * delta
        self.rect.y += self.velocity.y * delta

        self.check()

        ### Update ###
        self.hitbox = self.set_hitbox()

        ### Debug ###
        #   Hitbox
        # self.commands["debug"](self.debug_hitbox, self.debug_hitbox.set_position, (self.hitbox.x, self.hitbox.y))

    def check(self):
        for collider in self.collisions:
            if self.hitbox.colliderect(collider.hurtbox):
                # print(f"hit {collider.data.name}")
                collider.hurt(self.knockback)

                ### Debug ###
                #   Hitbox
                # self.debug_hitbox.kill()
                self.kill()

        if not self.timers["bullet_time"].active:
            ### Debug ###
            #   Hitbox
            # self.debug_hitbox.kill()
            self.kill()

    def set_hitbox(self):
        return self.rect.copy().inflate(BULLET_HITBOX_OFFSET)

    def update_timers(self):
        for timer in self.timers.values():
            timer.update()

    def update(self, delta):
        self.update_timers()
        self.move(delta)