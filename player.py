import pygame
from settings import *
from ray import *
from bullet import Bullet

class Player:
    def __init__(self, x, y,speed, mos_pos, image, dt):
        self.x = x
        self.y = y
        self.image = image
        self.mos_pos = mos_pos
        self.speed = speed
        self.dt = dt
        self.ray = Ray(self.x+self.image.get_width()/2, self.y, self.mos_pos[0],self.mos_pos[1])
        self.bullets = []
        self.health = 100
        self.mask = pygame.mask.from_surface(self.image)

        
    def update(self, screen):
        self.ray.end_x, self.ray.end_y = self.mos_pos[0],self.mos_pos[1]
        self.ray.start_x, self.ray.start_y = self.x+self.image.get_width()/2, self.y
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            self.x+=self.speed*self.dt
        if keys[pygame.K_a]:
            self.x-=self.speed*self.dt
        
        
        self.render(screen)
        
    def shoot(self):
        pew_pew = pygame.mixer.Sound("./assets/laser_pew.wav")
        pew_pew.play()
        bullet = Bullet(self.ray.start_x, self.ray.start_y,self.mos_pos[0],self.mos_pos[1], self.ray.angle, self.dt, 170)
        self.bullets.append(bullet)
        
    def render(self, screen):
        for bullet in self.bullets:
            if bullet.alive == True:
                bullet.update(screen)
            else:
                self.bullets.remove(bullet)
                # print("bullet died")

        screen.blit(self.image, (self.x, self.y))
        self.ray.update(screen)
        health_bar = pygame.Surface((2 if self.health<0 else self.health*2,10))
        health_bar.fill((0,255,0))
        screen.blit(health_bar, (20, WINDOW_HEIGHT-40))
        

