from settings import *
import pygame
import math

class Ray:
    def __init__(self, start_x, start_y, end_x, end_y, color=(255,0,0)):
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y
        self.color = color
        self.angle = math.atan2((self.end_y-self.start_y), (self.end_x-self.start_x))
        # print(self.end_x)
    def update(self, screen):
        self.angle = math.atan2((self.end_y-self.start_y), (self.end_x-self.start_x))
        # self.render(screen)

    def render(self, screen):
        pygame.draw.line(screen, self.color, (self.start_x, self.start_y), (self.end_x, self.end_y))