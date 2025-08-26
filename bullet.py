import pygame
from settings import *
import math

class Bullet:
    def __init__(self, start_x, start_y, end_x, end_y, angle, dt, speed=60, image=None):
        self.x, self.y = start_x, start_y
        self.start_x = start_x
        self.start_y = start_y
        
        # Calculate direction vector
        dx = end_x - start_x
        dy = end_y - start_y
        
        # Normalize the direction vector
        distance = math.sqrt(dx*dx + dy*dy)
        if distance > 0:
            self.dir_x = dx / distance
            self.dir_y = dy / distance
        else:
            self.dir_x = 1
            self.dir_y = 0
        
        self.angle = angle
        self.speed = speed
        self.dt = dt
        self.alive = True
        self.image = image
        self.rect = pygame.Surface((5, 5))
        
    def update(self, screen):
        # Check if bullet is outside window bounds
        if self.x > WINDOW_WIDTH or self.x < 0 or self.y < 0 or self.y > WINDOW_HEIGHT:
            self.alive = False
            
        if self.alive:
            # Move bullet in the calculated direction
            self.x += self.dir_x * self.speed * self.dt
            self.y += self.dir_y * self.speed * self.dt
            self.render(screen)
    
    def render(self, screen):
        self.rect.fill((255, 165, 0))
        screen.blit(self.rect, (self.x, self.y))