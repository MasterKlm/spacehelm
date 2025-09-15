import pygame, math
from settings import *
from enemy import *
import random
from timer import Timer

class Spawner:
    # Class-level shared resources to avoid loading multiple times
    _shared_sounds = None
    _shared_bullet_images = None
    
    @classmethod
    def initialize_shared_resources(cls):
        """Initialize shared resources once for all spawners"""
        if cls._shared_sounds is None:
            cls._shared_sounds = {
                "blaster": pygame.mixer.Sound("./assets/laser_pew.wav"),
                "sweeper": pygame.mixer.Sound("./assets/sweeper.wav")
            }
        
        if cls._shared_bullet_images is None:
            cls._shared_bullet_images = {
                "blaster": {
                    "original": pygame.transform.scale(
                        pygame.image.load('./assets/blaster_bullet_img.png').convert_alpha(), 
                        (10,10)
                    ),
                    "rotations": {}  # Cache for rotated versions
                },
                "sweeper": {
                    "original": pygame.transform.scale(
                        pygame.image.load('./assets/wave_bullet_img.png').convert_alpha(), 
                        (60,60)
                    ),
                    "rotations": {}  # Cache for rotated versions
                }
            }

    def __init__(self, num_enemies, dt, player, spawn_interval, enemy_type="ufo"):
        # Initialize shared resources
        self.initialize_shared_resources()
        
        self.num_enemies = num_enemies
        self.enemy_type = enemy_type
        self.enemies = []
        self.enemy_database = {
            "ufo":{
                "image": pygame.image.load("./assets/ufo.png").convert_alpha(),
                "gun_type":"blaster",
                "damage":5,
                "health":5,
                "shot_speed":40,
                "size": (40,40),
                "bullet_size":(30,30),
                "light":(200,0,0)

            },
            "orby":{
                "image": pygame.image.load("./assets/orby.png").convert_alpha(),
                "gun_type":"sweeper",
                "damage":15,
                "health":10,
                "shot_speed":30,
                "size": (50,50),
                "bullet_size":(80,80),
                
            }
        }
        self.dt = dt
        self.player = player
        self.current_enemy_image = pygame.transform.scale(
            self.enemy_database[self.enemy_type]["image"],
            self.enemy_database[self.enemy_type]["size"]
        )
        self.done_spawning = False
        self.spawn_count = 0
        self.spawn_timer = Timer(spawn_interval)
        self.spawn_timer.activate()
        
        # Cache masks for collision detection
        self.enemy_masks = {}
        for enemy_type, data in self.enemy_database.items():
            scaled_image = pygame.transform.scale(data["image"], data["size"])
            self.enemy_masks[enemy_type] = pygame.mask.from_surface(scaled_image)
        
        # Collision checking optimization
        self.collision_frame_counter = 0

    def update(self, screen):
        self.spawn_timer.update()
        
        if not self.done_spawning:
            if not self.spawn_timer.active and self.spawn_count < self.num_enemies:
                self.spawn(screen)
                self.spawn_count += 1
                self.spawn_timer.activate()
            
            if self.spawn_count == self.num_enemies:
                self.done_spawning = True
        
        # Only check collisions every 2nd frame to reduce load
        self.collision_frame_counter += 1
        check_collisions = (self.collision_frame_counter % 2 == 0)
        
        # Remove dead enemies first (more efficient)
        self.enemies = [enemy for enemy in self.enemies if enemy.alive]
        
        for enemy in self.enemies:
            # Update enemy
            enemy.update(screen)
            
            if not check_collisions:
                continue
                
            # Enemy bullets vs player - only check alive bullets
            alive_enemy_bullets = [b for b in enemy.gun.bullets if b.alive]
            for bullet in alive_enemy_bullets:
                # Fast distance check first
                dx = abs(bullet.x - (self.player.x + self.player.image.get_width()/2))
                dy = abs(bullet.y - (self.player.y + self.player.image.get_height()/2))
                
                if dx < 60 and dy < 60:  # Tighter bounds for better performance
                    # Use cached mask
                    offset = (int(bullet.x - self.player.x), int(bullet.y - self.player.y))
                    if self.player.mask.overlap(bullet.mask, offset):
                        self.player.health -= bullet.damage
                        bullet.alive = False
            
            # Player bullets vs enemy - only check alive bullets
            alive_player_bullets = [b for b in self.player.gun.bullets if b.alive]
            for bullet in alive_player_bullets:
                dx = abs(bullet.x - enemy.x)
                dy = abs(bullet.y - enemy.y)
                
                if dx < 35 and dy < 35:  # Tighter bounds
                    # Use cached mask
                    offset = (int(bullet.x - enemy.x), int(bullet.y - enemy.y))
                    enemy_mask = self.enemy_masks[self.enemy_type]
                    if enemy_mask.overlap(bullet.mask, offset):
                        enemy.health -= bullet.damage
                        enemy.show_health_bar()  # Show health bar when hit
                        bullet.alive = False
                        
                        if enemy.health <= 0:
                            enemy.alive = False
                        break  # Bullet hit, no need to check more bullets
        
    def spawn(self, screen):
        endX = random.randint(10, WINDOW_WIDTH-10)
        enemy = Enemy(
            random.randint(10, WINDOW_WIDTH-10),
            random.randint(10, WINDOW_HEIGHT//3),
            20, self.dt, self.player, endX,
            self.enemy_database[self.enemy_type], 
            self.current_enemy_image
        )
        
        # Pass shared resources to avoid reloading
        enemy.gun.shared_sounds = self._shared_sounds
        enemy.gun.shared_bullet_images = self._shared_bullet_images
        
        self.enemies.append(enemy)