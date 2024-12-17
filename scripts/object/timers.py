from scripts.autoload.constant import *

class Timer:
    def __init__(self, duration, func=None, repeat=False):
        self.duration = duration
        self.func = func
        self.time = 0
        self.active = False
        self.repeat = repeat

    def activate(self):
        self.active = True
        self.time = get_ticks()

    def deactivate(self):
        self.active = False
        self.time = 0
        if self.repeat:
            self.activate()

    def update(self):
        current_time = get_ticks()
        if current_time - self.time >= self.duration:
            if self.func and self.time != 0:
                print("execute function")
                self.func()
            self.deactivate()