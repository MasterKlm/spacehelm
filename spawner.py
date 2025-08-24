import pygame, math
from settings import *
from enemy import *
import random


class Spawner:
    def __init__(self, num_enemies, dt, player, enemy_type="ufo"):
        self.num_enemies= num_enemies
        self.enemy_type = enemy_type
        self.enemies = []
        self.enemy_images = {
            "ufo":pygame.image.load("./assets/ufo.png").convert_alpha(),

        }
        self.dt = dt
        self.player = player
        self.current_enemy_image = pygame.transform.scale(self.enemy_images[self.enemy_type], (40,40))
        self.done_spawning = False
        self.spawn_count = 0
    def update(self, screen):
        if self.done_spawning==False:
            
            if self.spawn_count<self.num_enemies:
                self.spawn(screen)
                self.spawn_count+=1
                if self.spawn_count==self.num_enemies:
                    self.done_spawning=True
        else:
            for enemy in self.enemies:
                if enemy.alive==True:
                    enemy_rect = enemy.image.get_rect()
                    enemy_mask = pygame.mask.from_surface(enemy.image)
                    mask_image = enemy_mask.to_surface()
                    # screen.blit(mask_image, (enemy.x,enemy.y))
                    
                    for bullet in self.player.bullets:
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
        enemy = Enemy(random.randint(10, WINDOW_WIDTH-10),20,20,self.dt, self.player,endX, self.current_enemy_image)
        enemy.update(screen)
        self.enemies.append(enemy)
     