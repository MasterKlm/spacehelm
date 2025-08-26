import pygame, math
from settings import *
from enemy import *
import random
from timer import Timer

class Spawner:
    def __init__(self, num_enemies, dt, player, spawn_interval, enemy_type="ufo"):
        self.num_enemies= num_enemies
        self.enemy_type = enemy_type
        self.enemies = []
        self.enemy_database = {
            "ufo":{
                "image": pygame.image.load("./assets/ufo.png").convert_alpha(),
                "gun_type":"blaster",
                "shot_speed":30
            },
            


        }
        self.dt = dt
        self.player = player
        self.current_enemy_image = pygame.transform.scale(self.enemy_database[self.enemy_type]["image"], (40,40))
        self.done_spawning = False
        self.spawn_count = 0
        self.spawn_timer = Timer(spawn_interval)
        self.spawn_timer.activate()

    def update(self, screen):
        self.spawn_timer.update()
        
        if self.done_spawning==False:
            
           if self.spawn_timer.active==False:
            if self.spawn_count<self.num_enemies:
                self.spawn(screen)
                self.spawn_count+=1
                self.spawn_timer.activate()

            if self.spawn_count==self.num_enemies:
                self.done_spawning=True
                
        for enemy in self.enemies:
            for bullet in enemy.gun.bullets:
                if bullet.alive == True:
                    bullet.update(screen)
                    bullet_mask = pygame.mask.from_surface(bullet.rect)
                    dx = (bullet.x-self.player.x)
                    dy = (bullet.y-self.player.y)
                    collision = self.player.mask.overlap(bullet_mask, (dx, dy))
                    if collision:
                        self.player.health-=1
                else:
                    enemy.gun.bullets.remove(bullet)

            if enemy.alive==True:
                enemy_rect = enemy.image.get_rect()
                enemy_mask = pygame.mask.from_surface(enemy.image)
                mask_image = enemy_mask.to_surface()
                    # screen.blit(mask_image, (enemy.x,enemy.y))
                    
                for bullet in self.player.gun.bullets:
                    bullet_mask = pygame.mask.from_surface(bullet.rect)
                    dx = (bullet.x-enemy.x)
                    dy = (bullet.y-enemy.y)
                    collision = enemy_mask.overlap(bullet_mask, (dx, dy))
                    if collision:
                        self.enemies.remove(enemy)
                        enemy.alive=False
                            



            else:
                pass                        
            enemy.update(screen)
    

        
    def spawn(self, screen):
        endX = random.randint(10, WINDOW_WIDTH-10)
        enemy = Enemy(random.randint(10, WINDOW_WIDTH-10),random.randint(10, WINDOW_HEIGHT/3),20,self.dt, self.player,endX,self.enemy_database[self.enemy_type], self.current_enemy_image)
        enemy.update(screen)
        self.enemies.append(enemy)
     