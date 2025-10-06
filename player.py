import pygame
import settings
from ray import *
from bullet import Bullet
from gun import Gun
from timer import Timer
import random


class Player:
    def __init__(self, x, y,speed, mos_pos, image, dt):
        self.x = x
        self.y = y
        self.image = image
        self.mos_pos = mos_pos
        self.speed = speed
        self.grid_id = random.randint(1,10**8)
        self.dt = dt
        self.ray = Ray(self.x+self.image.get_width()/2, self.y, self.mos_pos[0],self.mos_pos[1])
        self.health = 100
        self.mask = pygame.mask.from_surface(self.image)
        self.gun_index = 1
        # settings.spacialGrid.addClient(self.grid_id, x,y)
        self.sparks = []
        self.teleporter_timer = Timer(3000) 
        self.gun_data = {
            "1": {
                "gun_type": "blaster",
                "shot_speed": 80,
                "bullet_size": (30, 30),
                "shot_interval": 0,
                "penetration":0,
                "bullet_image": pygame.transform.smoothscale(pygame.image.load("./assets/images/blaster_bullet_img.png").convert_alpha(), (30, 30)),
                "light": (0, 0, 200),
                "gun_type_text_color":(0,0,200),
                "timer": Timer(0)  # Add individual timer
            },
            "2": {
                "gun_type": "rail",
                "shot_speed": 350,
                "bullet_size": (settings.WINDOW_HEIGHT, 200),
                "shot_interval": 5000,
                "penetration":0,
                "light": (144, 238, 144),
                "gun_type_text_color":(0,200,0),
                "timer": Timer(5000)  # Add individual timer
            },
            "3": {
                "gun_type": "sweeper",
                "shot_speed": 90,
                "bullet_size": (150, 150),
                "penetration":5,
                "bullet_image": pygame.transform.smoothscale(pygame.image.load("./assets/images/wave_bullet_img2.png").convert_alpha(), (150, 150)),
                "shot_interval": 2000,
                "gun_type_text_color": (160,32,240),
                "timer": Timer(2000)  # Add individual timer
            },

        }
        self.gun = Gun(self.gun_data[str(self.gun_index)], self.gun_data[str(self.gun_index)]["shot_interval"], self, self.gun_data[str(self.gun_index)]["shot_speed"])

        
    def update(self, screen):
        for i, spark in sorted(enumerate(self.sparks), reverse=True):
            spark.move(1)
            spark.draw(screen)
            if not spark.alive:
                self.sparks.pop(i)
                
        self.teleporter_timer.update()
        #teleporter reload icon
        # print("elapsed time: ", self.shot_timer.elapsed_time)

        start_angle = math.radians(0)
        # Calculate the proportion of time remaining (1.0 = full, 0.0 = empty)
        time_remaining_ratio = (self.teleporter_timer.duration - self.teleporter_timer.elapsed_time) / max(1, self.teleporter_timer.duration)

        # Convert to angle (360 degrees = full circle)
        end_angle = math.radians(360 * time_remaining_ratio)
        if end_angle != math.radians(360):
            pygame.draw.arc(screen, (173, 216, 230), pygame.Rect(self.x-50, self.y,30,30), start_angle, end_angle, 5)
        self.gun.gun_type_data = self.gun_data[str(self.gun_index)]
        self.gun.gun_type_name = self.gun_data[str(self.gun_index)]["gun_type"]
        self.gun.shot_speed = self.gun_data[str(self.gun_index)]["shot_speed"]
        self.gun.shot_interval = self.gun_data[str(self.gun_index)]["shot_interval"]
        # print("Player Gun name: ", self.gun.gun_type_name)
        self.ray.end_x, self.ray.end_y = self.mos_pos[0],self.mos_pos[1]
        self.ray.start_x, self.ray.start_y = self.x+self.image.get_width()/2, self.y
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            pygame.quit()
        if keys[pygame.K_d] and self.x < settings.WINDOW_WIDTH-45:
            # settings.spacialGrid.moveClient(self.grid_id, self.x, self.y, self.x + self.speed*self.dt, self.y +self.speed*self.dt)

            self.x+=self.speed*self.dt
        if keys[pygame.K_w] and self.y > settings.WINDOW_HEIGHT/2:
            # settings.spacialGrid.moveClient(self.grid_id, self.x, self.y, self.x + self.speed*self.dt, self.y +self.speed*self.dt)
            self.y-=self.speed*self.dt
        if keys[pygame.K_s] and self.y < settings.WINDOW_HEIGHT-45:
            # settings.spacialGrid.moveClient(self.grid_id, self.x, self.y, self.x + self.speed*self.dt, self.y +self.speed*self.dt)
            self.y+=self.speed*self.dt
        if keys[pygame.K_a] and self.x > 5:
            # settings.spacialGrid.moveClient(self.grid_id, self.x, self.y, self.x + self.speed*self.dt, self.y +self.speed*self.dt)
            self.x-=self.speed*self.dt
        if keys[pygame.K_1]:
            self.gun_index = 1
        if keys[pygame.K_2]:
            self.gun_index = 2
        if keys[pygame.K_3]:
            self.gun_index = 3
        
        
        self.render(screen)
        self.gun.update(screen)
        
    
    def render(self, screen):
        
                # print("bullet died")

        screen.blit(self.image, (self.x, self.y))
        self.ray.update(screen)
        health_bar = pygame.Surface((2 if self.health<0 else self.health*2,10))
        health_bar.fill((0,255,0))
        screen.blit(health_bar, (20, settings.WINDOW_HEIGHT-40))
        

