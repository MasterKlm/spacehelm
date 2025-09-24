import pygame
from settings import *
from ray import *
from bullet import Bullet
from gun import Gun
from timer import Timer

class Player:
    def __init__(self, x, y,speed, mos_pos, image, dt):
        self.x = x
        self.y = y
        self.image = image
        self.mos_pos = mos_pos
        self.speed = speed
        self.dt = dt
        self.ray = Ray(self.x+self.image.get_width()/2, self.y, self.mos_pos[0],self.mos_pos[1])
        self.health = 100
        self.mask = pygame.mask.from_surface(self.image)
        self.gun_index = 1
        self.gun_data = {
            "1": {
                "gun_type": "blaster",
                "shot_speed": 80,
                "bullet_size": (30, 30),
                "shot_interval": 0,
                "bullet_image": pygame.transform.scale(pygame.image.load("./assets/blaster_bullet_img.png").convert_alpha(), (30, 30)),
                "light": (0, 0, 200),
                "timer": Timer(0)  # Add individual timer
            },
            "2": {
                "gun_type": "rail",
                "shot_speed": 350,
                "bullet_size": (WINDOW_HEIGHT, 200),
                "shot_interval": 5000,
                "light": (144, 238, 144),
                "timer": Timer(5000)  # Add individual timer
            }
        }
        self.gun = Gun(self.gun_data[str(self.gun_index)], self.gun_data[str(self.gun_index)]["shot_interval"], self, self.gun_data[str(self.gun_index)]["shot_speed"])

        
    def update(self, screen):

        self.gun.gun_type_data = self.gun_data[str(self.gun_index)]
        self.gun.gun_type_name = self.gun_data[str(self.gun_index)]["gun_type"]
        self.gun.shot_speed = self.gun_data[str(self.gun_index)]["shot_speed"]
        self.gun.shot_interval = self.gun_data[str(self.gun_index)]["shot_interval"]
        # print("Player Gun name: ", self.gun.gun_type_name)
        self.ray.end_x, self.ray.end_y = self.mos_pos[0],self.mos_pos[1]
        self.ray.start_x, self.ray.start_y = self.x+self.image.get_width()/2, self.y
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d] and self.x < WINDOW_WIDTH-45:
            self.x+=self.speed*self.dt
        if keys[pygame.K_w] and self.y > WINDOW_HEIGHT/2:
            self.y-=self.speed*self.dt
        if keys[pygame.K_s] and self.y < WINDOW_HEIGHT-45:
            self.y+=self.speed*self.dt
        if keys[pygame.K_a] and self.x > 5:
            self.x-=self.speed*self.dt
        if keys[pygame.K_1]:
            self.gun_index = 1
        if keys[pygame.K_2]:
            self.gun_index = 2
        
        
        self.render(screen)
        self.gun.update(screen)
        
    
    def render(self, screen):
        
                # print("bullet died")

        screen.blit(self.image, (self.x, self.y))
        self.ray.update(screen)
        health_bar = pygame.Surface((2 if self.health<0 else self.health*2,10))
        health_bar.fill((0,255,0))
        screen.blit(health_bar, (20, WINDOW_HEIGHT-40))
        

