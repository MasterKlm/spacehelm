import pygame
from settings import *
import math

class Bullet: 
    def __init__(self, start_x, start_y, end_x, end_y, angle,  dt,speed=60, image=None):
        self.x, self.y, = start_x, start_y
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y
        dx = self.end_x - self.start_x
        dy = self.end_y - self.start_y
        self.end_x = start_x + dx * 2
        self.end_y = start_y + dy * 2
        self.angle = angle
        self.speed = speed
        self.dt = dt
        self.alive = True
        self.image = image
        self.rect = pygame.Surface((5,5))
        
    def update(self, screen):
        # print(self.start_x)
        self.angle = math.atan2((self.end_y-self.y), (self.end_x-self.x))
        # print(f"end_x: {self.x}, end_y: {self.y}, angle: {self.angle}")

        if self.x>WINDOW_WIDTH or self.x<0 or self.y<0 or self.y > WINDOW_HEIGHT:
            self.alive = False
        if self.alive:
            self.x += math.cos(self.angle)*self.speed*self.dt
            self.y -= -math.sin(self.angle)*self.speed*self.dt
            self.render(screen)

    def render(self, screen):
        
        self.rect.fill((255,165,0))
        screen.blit(self.rect, (self.x,self.y))


        