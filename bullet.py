import pygame
import settings
import math
from ambient import create_light_surface
import helpers
import random

class Bullet:
    def __init__(self, start_x, start_y, end_x, end_y, angle, dt, damage,bullet_image,size, gun_type_name,penetration=0, speed=60, lightColor=None, cachedLightSurface=None, rectForwardAngle=None, ):
        self.x, self.y = start_x, start_y
        self.start_x = start_x
        self.start_y = start_y
        self.bullet_image = bullet_image
        self.damage = damage
        self.gun_type_name = gun_type_name
        self.size = size
        self.rectForwardAngle = rectForwardAngle
        self.lightColor = lightColor
        self.penetration = penetration
        self.hit_count = 0
        self.grid_id = random.randint(1,10**8)
        settings.spacialGrid.addClient(self.grid_id, self.x, self.y, self, "bullet")


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
        # self.rect = pygame.Surface((5, 5))
        self.surface = bullet_image if bullet_image!=None else pygame.Surface((5, 5)) if self.gun_type_name != "rail" else pygame.Surface((10, settings.WINDOW_HEIGHT), pygame.SRCALPHA)
        self.mask = pygame.mask.from_surface(self.surface)
        self.rect = None
        self.lightRadius = int(math.hypot(self.dir_x * self.speed * self.dt, self.dir_y * self.speed * self.dt)) // 2 if gun_type_name == "rail" else round(self.bullet_image.get_width()/0.5)
        
        if self.bullet_image is not None and lightColor== None:
            avg_color = helpers.get_average_color(self.bullet_image)
        else:
            avg_color = lightColor  # fallback

        self.light_surface = cachedLightSurface if cachedLightSurface!=None else create_light_surface(self.lightRadius, avg_color)
        
    def update(self, screen):
        # Check if bullet is outside window bounds
        if ((self.x + self.bullet_image.get_width() if self.bullet_image != None else 0) > settings.WINDOW_WIDTH+100) or (self.x < 0) or (self.y < 0) or (self.y+self.bullet_image.get_height() if self.bullet_image != None else 0) > settings.WINDOW_HEIGHT+150:
            self.alive = False
            settings.spacialGrid.removeClient(self.grid_id, self.x, self.y)
            
        if self.alive:
            # Move bullet in the calculated direction
            new_x = self.x + self.dir_x * self.speed * self.dt
            new_y = self.y + self.dir_y * self.speed * self.dt
            settings.spacialGrid.moveClient(self.grid_id, self.x, self.y, new_x,new_y)
            self.x = new_x
            self.y = new_y
            self.render(screen)
    
    def render(self, screen):
        if self.bullet_image is not None:
            screen.blit(self.bullet_image, (self.x, self.y))
            screen.blit(
                self.light_surface,
                (self.x + self.size[0] // 2 - self.lightRadius, self.y + self.size[1] // 2 - self.lightRadius),
                special_flags=pygame.BLEND_RGB_ADD
            )
        else:
            if self.gun_type_name == "blaster":
                pygame.draw.rect(screen, (255, 165, 0), (self.x, self.y, 5, 5))
                screen.blit(
                    self.light_surface,
                    (self.x + self.size[0] // 2 - self.lightRadius, self.y + self.size[1] // 2 - self.lightRadius),
                    special_flags=pygame.BLEND_RGB_ADD
                )
            if self.gun_type_name == "rail":
                # Draw the red rect on a fresh surface each frame, then rotate and blit
                base_surface = pygame.Surface((10, 200), pygame.SRCALPHA)
                # self.lightRadius = base_surface.get_width() *4
                # self.light_surface = create_light_surface(self.lightRadius, self.lightColor)
                pygame.draw.rect(base_surface, (0, 255,0), base_surface.get_rect())
                # Draw the circle at the center-top of the base_surface
                pygame.draw.rect(base_surface, (0, 0, 0), pygame.Rect(0, 0, 10,4))
                pygame.draw.circle(base_surface, (0, 255,0), (base_surface.get_width() // 2, 5), 5,0,True, True)
                

                #inner circle post processing effect:
                pygame.draw.rect(base_surface, (144, 238, 144), base_surface.get_rect().inflate(-4,-4))
                # Draw the circle at the center-top of the base_surface
                # pygame.draw.rect(base_surface, (0, 0, 0), pygame.Rect(0, 0, 10,4))
                pygame.draw.circle(base_surface, (144, 238, 144), (base_surface.get_width() // 2, 5), 1,0,True, True)


                rotation_degrees = -math.degrees(self.angle-self.rectForwardAngle)
                rotated_surface = pygame.transform.rotate(base_surface, rotation_degrees)
                rotated_rect = rotated_surface.get_rect(center=(self.x, self.y))
                self.surface = rotated_surface
                self.rect = rotated_surface.get_rect(topleft=(self.x,self.y))
                screen.blit(rotated_surface, rotated_rect.topleft)
                # screen.blit(
                #     self.light_surface,
                #     (rotated_rect.topleft[0] + base_surface.get_width() // 2 - self.lightRadius, rotated_rect.topleft[1] + base_surface.get_height() // 2 - self.lightRadius),
                #     special_flags=pygame.BLEND_RGB_ADD
                # )

