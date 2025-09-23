import pygame, math
from settings import *
from ray import Ray
import random
from timer import Timer
from bullet import get_average_color
from gun import Gun

class Enemy:
    def __init__(self, x, y, speed, dt, player, endX, endY, enemy_type_data, image):
        self.x = x
        self.y = y
        self.dt = dt
        self.image = image
        self.alive = True
        self.player = player
        self.end_x = endX
        self.end_y = endY
        self.speed = speed
        self.health = enemy_type_data["health"]
        self.max_health = enemy_type_data["health"]  # Store original health for health bar calculation
        self.keep_moving = True
        self.ray = Ray(self.x-self.image.get_width()/2, self.y+self.image.get_height()/2, self.player.x+self.player.image.get_width()/2, self.player.y, (0,255,0))
        self.gun = Gun(enemy_type_data, 3000, self, enemy_type_data["shot_speed"], True)
        self.image_average_color = get_average_color(self.image)
        # Health bar properties
        self.show_health_bar_flag = False
        self.health_bar_timer = Timer(2000)  # Show health bar for 2 seconds
        self.health_bar_width = 40
        self.health_bar_height = 6

    def show_health_bar(self):
        """Activate the health bar display when enemy is hit"""
        self.show_health_bar_flag = True
        self.health_bar_timer.activate()

    def update(self, screen):
        self.move()
        self.render(screen)
        self.gun.update(screen)
        
        # Update health bar timer
        if self.show_health_bar_flag:
            self.health_bar_timer.update()
            if not self.health_bar_timer.active:
                self.show_health_bar_flag = False
 
    def move(self):
        if self.keep_moving:
            diff_x = self.end_x - self.x
            diff_y = self.end_y - self.y
            distance = math.hypot(diff_x, diff_y)
            if distance < 50:
                self.keep_moving = False
                self.end_x = random.randint(10, WINDOW_WIDTH-10)
                self.end_y = random.randint(10, WINDOW_HEIGHT//3)
            else:
                move_speed = self.speed * self.dt
                # Normalize direction
                if distance != 0:
                    norm_x = diff_x / distance
                    norm_y = diff_y / distance
                else:
                    norm_x = 1
                    norm_y = 0
                self.x += norm_x * move_speed
                self.y += norm_y * move_speed
        else:
            self.keep_moving = True

    def render_health_bar(self, screen):
        """Render the health bar above the enemy"""
        if not self.show_health_bar_flag:
            return
            
        # Calculate health bar position (above the enemy)
        bar_x = self.x + (self.image.get_width() - self.health_bar_width) // 2
        bar_y = self.y - 15
        
        # Background (red) bar
        background_rect = pygame.Rect(bar_x, bar_y, self.health_bar_width, self.health_bar_height)
        pygame.draw.rect(screen, (255, 0, 0), background_rect)
        
        # Health (green) bar
        health_percentage = max(0, self.health / self.max_health)
        health_width = int(self.health_bar_width * health_percentage)
        
        if health_width > 0:
            health_rect = pygame.Rect(bar_x, bar_y, health_width, self.health_bar_height)
            pygame.draw.rect(screen, (0, 255, 0), health_rect)
        
        # Border
        pygame.draw.rect(screen, (255, 255, 255), background_rect, 1)

    def render(self, screen):
        screen.blit(self.image, (self.x, self.y))
        self.render_health_bar(screen)
        # self.ray.render(screen)