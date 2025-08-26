import pygame
from bullet import Bullet
from timer import Timer


class Gun:
    def __init__(self, gun_type, damage, shot_interval, entity, shot_speed,  auto_shoot=False):
        self.gun_type = gun_type
        self.damage = damage
        self.shot_interval = shot_interval
        self.shot_timer = Timer(shot_interval)
        self.entity = entity
        self.auto_shoot = auto_shoot
        self.shot_speed = gun_type["shot_speed"]
        # self.shot_timer.activate()
        self.bullets = []
        self.sounds = {
            "blaster": pygame.mixer.Sound("./assets/laser_pew.wav")
        }
        if self.auto_shoot:
            self.shot_timer.activate()
            
            
    def update(self, screen):
        if self.shot_interval != 0:
            self.shot_timer.update()
            if self.auto_shoot:
                if self.shot_timer.active == False:
                    self.shoot()
                    self.shot_timer.activate()



        for bullet in self.bullets:
            if bullet.alive == True:
                bullet.update(screen)
            else:
                self.bullets.remove(bullet)

    def shoot(self):
        
        if self.shot_timer.active==False and self.shot_interval!=0:
            self.sounds[self.gun_type["gun_type"]].play()
            bullet = Bullet(self.entity.ray.start_x, self.entity.ray.start_y,self.entity.ray.end_x,self.entity.ray.end_y, self.entity.ray.angle, self.entity.dt, self.shot_speed)
            self.bullets.append(bullet)
            self.shot_timer.activate()
        if self.shot_interval==0:
            self.sounds[self.gun_type["gun_type"]].play()
            bullet = Bullet(self.entity.ray.start_x, self.entity.ray.start_y,self.entity.ray.end_x,self.entity.ray.end_y, self.entity.ray.angle, self.entity.dt, self.shot_speed)
            self.bullets.append(bullet)
            self.shot_timer.activate()
        