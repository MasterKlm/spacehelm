import pygame, math
from settings import *
from ray import Ray
import random
from timer import Timer
from bullet import Bullet
from gun import Gun

class Enemy:
    def __init__(self, x, y, speed, dt,player,endX,gun_type_data, image):
        self.x = x
        self.y = y
        self.dt = dt
        self.image = image
        self.alive = True
        self.player = player
        self.end_x = endX
        self.speed = speed
        self.keep_moving = True
        self.ray = Ray(self.x+self.image.get_width()/2, self.y+self.image.get_height()/2, self.player.x+self.player.image.get_width()/2, self.player.y, (0,255,0))
        self.gun = Gun(gun_type_data, 5, 3000, self,gun_type_data["shot_speed"], True)


    def update(self, screen):
        # print(f"end_x:{self.end_x}, self.x:{self.x}")
        
        self.ray.start_x = self.x+self.image.get_width()/2
        self.ray.start_y = self.y+self.image.get_height()/2
        self.ray.end_x = self.player.x+self.player.image.get_width()/2
        self.ray.end_y = self.player.y
        self.move()
        self.render(screen)
        self.gun.update(screen)
        # self.ray.render(screen)
 
    def move(self):
        dif = max(self.x, self.end_x)-min(self.x, self.end_x)
        if dif<50:
            self.keep_moving=False
        else:
            self.keep_moving=True
        if self.keep_moving:
            if self.x<self.end_x:
                self.x+=self.speed*self.dt
            if self.x>self.end_x:
                self.x-=self.speed*self.dt
        else:
            self.end_x = random.randint(10, WINDOW_WIDTH-10)
        

    def render(self, screen):
        
                # print("bullet died")
        screen.blit(self.image, (self.x, self.y))
        
