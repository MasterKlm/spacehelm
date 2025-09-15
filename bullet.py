import pygame
from settings import *
import math
from ambient import create_light_surface

def get_average_color(surface):
    arr = pygame.surfarray.pixels3d(surface)
    if surface.get_masks()[3] != 0:  # Has alpha
        alpha = pygame.surfarray.pixels_alpha(surface)
        mask = alpha > 0
        if mask.any():
            r = arr[:,:,0][mask].mean()
            g = arr[:,:,1][mask].mean()
            b = arr[:,:,2][mask].mean()
        else:
            r = g = b = 0
    else:
        r = arr[:,:,0].mean()
        g = arr[:,:,1].mean()
        b = arr[:,:,2].mean()
    return (int(r), int(g), int(b))

class Bullet:
    def __init__(self, start_x, start_y, end_x, end_y, angle, dt, damage,bullet_image,size, speed=60, lightColor=None):
        self.x, self.y = start_x, start_y
        self.start_x = start_x
        self.start_y = start_y
        self.bullet_image = bullet_image
        self.damage = damage
        self.size = size
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
        self.surface = bullet_image if bullet_image!=None else pygame.Surface((5, 5))
        self.mask = pygame.mask.from_surface(self.surface)
        self.lightRadius = 50
        
        if self.bullet_image is not None and lightColor== None:
            avg_color = get_average_color(self.bullet_image)
        else:
            avg_color = lightColor  # fallback

        self.light_surface = create_light_surface(self.lightRadius, avg_color)
        
    def update(self, screen):
        # Check if bullet is outside window bounds
        if self.x > WINDOW_WIDTH or self.x < 0 or self.y < 0 or self.y > WINDOW_HEIGHT:
            self.alive = False
            
        if self.alive:
            # Move bullet in the calculated direction
            self.x += self.dir_x * self.speed * self.dt
            self.y += self.dir_y * self.speed * self.dt
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
            pygame.draw.rect(screen, (255, 165, 0), (self.x, self.y, 5, 5))
