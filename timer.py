from pygame.time import get_ticks


class Timer:
    def __init__(self, duration):
        self.duration = duration
        self.start_time = 0
        self.active = False
    def deactivate(self):
        self.active = False
        self.start_time=0
    def update(self):
        if self.active:
            current_time = get_ticks()
            if current_time - self.start_time >= self.duration:
                self.deactivate()
        else:      
            current_time = get_ticks()
            if current_time - self.start_time >= 1000:
                    self.activate()
    def activate(self):
        self.active = True
        self.start_time = get_ticks()