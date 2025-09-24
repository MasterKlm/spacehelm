import pygame
from bullet import Bullet
from timer import Timer
import math


class Gun:
    def __init__(self, gun_type_data, shot_interval, entity, shot_speed, auto_shoot=False):
        self.gun_type_name = gun_type_data["gun_type"]
        self.gun_type_data = gun_type_data
        self.shot_interval = shot_interval
        self.last_shot_interval = shot_interval
        self.shot_timer = Timer(shot_interval)
        self.entity = entity
        self.auto_shoot = auto_shoot
        self.shot_speed = shot_speed
        self.cached_bullets_light = {}
        # These will be set by the spawner to avoid loading resources multiple times
        self.shared_sounds = None
        self.shared_bullet_images = None
        # Fallback bullet data (only used if shared resources not available)
        self.bullet_data = {
            "blaster": {
                "image": self.gun_type_data["bullet_image"] if "bullet_image" in self.gun_type_data else None,  # Will be loaded from shared resources
                "forward_angle": 200 ,
                "damage":5
            },
            "sweeper": {
                "image": self.gun_type_data["bullet_image"] if "bullet_image" in self.gun_type_data else None,  # Will be loaded from shared resources
                "forward_angle": 270,
                "damage":15

            },
            "rail": {
                "image":self.gun_type_data["bullet_image"] if "bullet_image" in self.gun_type_data else None, # Will be loaded from shared resources
                "forward_angle": 300,
                "damage":15

            }
        }
        
        self.bullets = []
        
        # Fallback sounds (only used if shared resources not available)
        self.sounds = {}
        
        if self.auto_shoot:
            self.shot_timer.activate()
    
    def get_rotated_bullet_image(self, target_angle):
        """Get bullet image rotated to face the target angle with caching and scaling"""
        
        # Rail gun should not have an image - always return None
        if self.gun_type_name == "rail":
            return None
        
        # Use shared resources if available, but first check if gun_type_data has bullet_image
        if self.gun_type_data and "bullet_image" in self.gun_type_data:
            original_image = self.gun_type_data["bullet_image"]  # Get directly from gun_type_data

            forward_angle_rad = math.radians(self.bullet_data[self.gun_type_name]["forward_angle"])
            rotation_needed = target_angle - forward_angle_rad
            rotation_degrees = -math.degrees(rotation_needed)
            # Rotate and cache
            rotated_image = pygame.transform.rotate(original_image, rotation_degrees)
            return rotated_image

        # Fallback to old method if shared resources not available
        return self._get_fallback_bullet_image(target_angle)
    
    def _get_fallback_bullet_image(self, target_angle):
        """Fallback method for bullet image rotation and scaling"""
        if self.bullet_data[self.gun_type_name]["image"] is None:
            # Load image only once, but scale to bullet_size
            bullet_size = self.gun_type_data["bullet_size"] if "bullet_size" in self.gun_type_data else (30, 30)
            if self.gun_type_name == "blaster":
                self.bullet_data[self.gun_type_name]["image"] = pygame.transform.scale(
                    pygame.image.load('./assets/blaster_bullet_img.png').convert_alpha(), bullet_size
                )
            elif self.gun_type_name == "sweeper":
                self.bullet_data[self.gun_type_name]["image"] = pygame.transform.scale(
                    pygame.image.load('./assets/wave_bullet_img.png').convert_alpha(), bullet_size
                )
            elif self.gun_type_name == "rail":
                self.bullet_data[self.gun_type_name]["image"] = None
        original_image = self.bullet_data[self.gun_type_name]["image"]
        if original_image is None:
            return None
        forward_angle_rad = math.radians(self.bullet_data[self.gun_type_name]["forward_angle"])
        rotation_needed = target_angle - forward_angle_rad
        rotation_degrees = -math.degrees(rotation_needed)
        # Already scaled, just rotate
        # from player import Player
        # if (isinstance(self.entity, Player )):
        #     print("using fall back image")

        return pygame.transform.rotate(original_image, rotation_degrees)
    
    def play_sound(self, gun_type_name):
        """Play gun sound using shared resources if available"""
        if self.shared_sounds and self.gun_type_name in self.shared_sounds:
            self.shared_sounds[self.gun_type_name].set_volume(0.1)
            self.shared_sounds[self.gun_type_name].play()
        else:
            # Fallback: load sound if not already loaded
            if self.gun_type_name not in self.sounds:
                if self.gun_type_name == "blaster":
                    self.sounds[self.gun_type_name] = pygame.mixer.Sound("./assets/laser_pew.wav")
                elif self.gun_type_name == "sweeper":
                    self.sounds[self.gun_type_name] = pygame.mixer.Sound("./assets/sweeper.wav")
            
            if self.gun_type_name in self.sounds:
                self.sounds[self.gun_type_name].set_volume(0.1)
                self.sounds[self.gun_type_name].play()
    
    def update(self, screen):
        if self.shot_interval != self.last_shot_interval:
            self.shot_timer = Timer(self.shot_interval)
            self.last_shot_interval = self.shot_interval
        from player import Player
        if isinstance(self.entity, Player):
            self.gun_type_data = self.entity.gun_data[str(self.entity.gun_index)] 
        if self.shot_interval != 0:
            self.shot_timer.update()
            if self.auto_shoot:
                if self.shot_timer.active == False:
                    from enemy import Enemy
                    if isinstance(self.entity, Enemy):
                        self.entity.ray.start_x = self.entity.x + self.entity.image.get_width()/2
                        self.entity.ray.start_y = self.entity.y + self.entity.image.get_height()/2
                        self.entity.ray.end_x = self.entity.player.x + self.entity.player.image.get_width()/2
                        self.entity.ray.end_y = self.entity.player.y
                    self.shoot()
                    
                    self.shot_timer.activate()
        
        # More efficient bullet cleanup
        self.bullets = [bullet for bullet in self.bullets if bullet.alive]
        
        for bullet in self.bullets:
            bullet.update(screen)
    
    def shoot(self):
   
        
        if self.shot_timer.active == False and self.shot_interval != 0:
            self.play_sound(self.gun_type_name)
            # Get the rotated bullet image for the current ray angle
            bullet_image = self.get_rotated_bullet_image(self.entity.ray.angle)
            
            bullet = Bullet(
                self.entity.ray.start_x, 
                self.entity.ray.start_y,
                self.entity.ray.end_x,
                self.entity.ray.end_y, 
                self.entity.ray.angle, 
                self.entity.dt, 
                self.bullet_data[self.gun_type_name]["damage"],
                bullet_image,
                self.gun_type_data["bullet_size"],
                self.gun_type_name,
                self.shot_speed,
                self.gun_type_data["light"] if "light" in self.gun_type_data else None,
                self.cached_bullets_light[self.gun_type_name] if self.gun_type_name in self.cached_bullets_light else None,
                self.bullet_data[self.gun_type_name]["forward_angle"]
               
            )
            if self.gun_type_name in self.cached_bullets_light:
                # print("cached light exist")
                pass
            else:
                # print("cached light addded")

                self.cached_bullets_light[self.gun_type_name] = bullet.light_surface
            self.bullets.append(bullet)
            self.shot_timer.activate()
        
        if self.shot_interval == 0:
            self.play_sound(self.gun_type_name)
            
            # Get the rotated bullet image for the current ray angle
            bullet_image = self.get_rotated_bullet_image(self.entity.ray.angle)

            bullet = Bullet(
                self.entity.ray.start_x, 
                self.entity.ray.start_y,
                self.entity.ray.end_x,
                self.entity.ray.end_y, 
                self.entity.ray.angle, 
                self.entity.dt, 
                self.bullet_data[self.gun_type_name]["damage"],
                bullet_image,
                self.gun_type_data["bullet_size"],
                self.gun_type_name,
                self.shot_speed,
                self.gun_type_data["light"] if "light" in self.gun_type_data else None,
                self.cached_bullets_light[self.gun_type_name] if self.gun_type_name in self.cached_bullets_light else None,
                self.bullet_data[self.gun_type_name]["forward_angle"]
      
            )
            if self.gun_type_name in self.cached_bullets_light:
                # print("cached light exist")
                pass
            else:
                # print("cached light addded")

                self.cached_bullets_light[self.gun_type_name] = bullet.light_surface
            self.bullets.append(bullet)
            self.shot_timer.activate()