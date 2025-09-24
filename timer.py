from pygame.time import get_ticks


class Timer:
    def __init__(self, duration):
        self.duration = duration
        self.start_time = 0
        self.active = False
        self.elapsed_time = 0
    def deactivate(self):
        self.active = False
        self.start_time=0
        self.elapsed_time = 0

    def update(self):
        if self.active:
            current_time = get_ticks()
            self.elapsed_time = current_time - self.start_time
            if self.elapsed_time >= self.duration:
                self.deactivate()
        
    def activate(self):
        self.active = True
        self.start_time = get_ticks()