import pygame, math
from settings import *
from enemy import *
import random
from timer import Timer
from spark import Spark

class Spawner:
    # Class-level shared resources to avoid loading multiple times
    _shared_sounds = None
    _shared_bullet_images = None
    
    @classmethod
    def initialize_shared_resources(cls):
        """Initialize shared resources once for all spawners"""
        if cls._shared_sounds is None:
            cls._shared_sounds = {
                "blaster": pygame.mixer.Sound("./assets/sounds/laser_pew.wav"),
                "sweeper": pygame.mixer.Sound("./assets/sounds/sweeper.wav")
            }
        
        if cls._shared_bullet_images is None:
            cls._shared_bullet_images = {
                "blaster": {
                    "original": pygame.transform.scale(
                        pygame.image.load('./assets/images/blaster_bullet_img.png').convert_alpha(), 
                        (10,10)
                    ),
                    "rotations": {}  # Cache for rotated versions
                },
                "sweeper": {
                    "original": pygame.transform.scale(
                        pygame.image.load('./assets/images/wave_bullet_img.png').convert_alpha(), 
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
                "image": pygame.image.load("./assets/images/ufo.png").convert_alpha(),
                "gun_type":"blaster",
                "damage":5,
                "name": "ufo",
                "health":5,
                "speed":1.2,
                "shot_speed":30,
                "size": (40,40),
                "bullet_size":(30,30),
                "light":(200,0,0),
                "bullet_image": pygame.transform.scale(pygame.image.load("./assets/images/blaster_bullet_img.png").convert_alpha(), (30,30)),

            },
            "orby":{
                "image": pygame.image.load("./assets/images/orby.png").convert_alpha(),
                "gun_type":"sweeper",
                "damage":15,
                "health":10,
                "speed":1,
                "shot_speed":40,
                "name": "orby",
                "size": (50,50),
                "bullet_size":(80,80),
                "bullet_image": pygame.transform.smoothscale(pygame.image.load("./assets/images/wave_bullet_img.png").convert_alpha(), (80,80)),
                "light":(255,165,0),
                
            },
            "orbyprime":{
                "image": pygame.image.load("./assets/images/orbyprimephase1.png").convert_alpha(),
                "gun_type":"sweeper",
                "damage":20,
                "health":400,
                "shot_speed":42,
                "speed":2.6,
                "name": "orbyprime",
                "size": (150,150),
                "bullet_size":(50,50),
                "enemy_aura": True,
                "bullet_image": pygame.transform.smoothscale(pygame.image.load("./assets/images/wave_bullet_img.png").convert_alpha(), (50,50)),
                "light":(255,165,0),
                
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
        self.sparks = []
        # Cache masks for collision detection
        self.enemy_masks = {}
        for enemy_type, data in self.enemy_database.items():
            scaled_image = pygame.transform.scale(data["image"], data["size"])
            self.enemy_masks[enemy_type] = pygame.mask.from_surface(scaled_image)
        
        # Collision checking optimization
        self.collision_frame_counter = 0

    def update(self, screen):
        self.spawn_timer.update()
        for i, spark in sorted(enumerate(self.sparks), reverse=True):
            spark.move(1)
            spark.draw(screen)
            if not spark.alive:
                self.sparks.pop(i)
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
            

            # Enemy bullets vs player - only check alive bullets
            alive_enemy_bullets = [b for b in enemy.gun.bullets if b.alive]
            for bullet in alive_enemy_bullets:
                player_ids = settings.spacialGrid.getNearbyByType(bullet.x, bullet.y, "player")
                # print("nearby players: ",player_ids)
                for player_id in player_ids:
                    player, _ = settings.spacialGrid.entity_registry[player_id]

                    # Use cached mask
                    offset = (int(bullet.x -player.x), int(bullet.y -player.y))
                    if player.mask.overlap(bullet.mask, offset):
                        self.sparks.append(Spark([self.player.x,player.y], math.radians(random.randint(20, 130)), random.randint(3, 6), (255, 0, 0), 3))
                        self.sparks.append(Spark([self.player.x,player.y], math.radians(random.randint(20, 130)), random.randint(3, 6), (255, 0, 0), 2))
                        self.sparks.append(Spark([self.player.x,player.y], math.radians(random.randint(20, 130)), random.randint(3, 6), (255, 0, 0), 4))
                        self.sparks.append(Spark([self.player.x,player.y], math.radians(random.randint(20, 130)), random.randint(3, 6), (255, 0, 0), 2))
                        self.sparks.append(Spark([self.player.x,player.y], math.radians(random.randint(20, 130)), random.randint(3, 6), (255, 0, 0), 3))
                        player.health -= bullet.damage
                        if player.health <= 0:
                            self.sparks.append(Spark([self.player.x,player.y], math.radians(random.randint(0, 360)), random.randint(3, 6), (255, 0, 0), 5))
                            self.sparks.append(Spark([self.player.x,player.y], math.radians(random.randint(0, 360)), random.randint(3, 6), (255, 0, 0), 2))
                            self.sparks.append(Spark([self.player.x,player.y], math.radians(random.randint(0, 360)), random.randint(3, 6), (255, 165, 0), 4))
                            self.sparks.append(Spark([self.player.x,player.y], math.radians(random.randint(0, 360)), random.randint(3, 6), (255, 0, 0), 8))
                            self.sparks.append(Spark([self.player.x,player.y], math.radians(random.randint(0, 360)), random.randint(3, 6), (255, 0, 0), 10))
                            self.sparks.append(Spark([self.player.x,player.y], math.radians(random.randint(0, 360)), random.randint(3, 6), (255, 0, 0), 4))
                            self.sparks.append(Spark([self.player.x,player.y], math.radians(random.randint(0, 360)), random.randint(3, 6), (255, 165, 0), 10))
                            self.sparks.append(Spark([self.player.x,player.y], math.radians(random.randint(0, 360)), random.randint(3, 6), (255, 0, 0), 10))
                            self.sparks.append(Spark([self.player.x,player.y], math.radians(random.randint(0, 360)), random.randint(3, 6), (255, 165, 0), 7))
                            settings.spacialGrid.removeClient(player.grid_id, player.x, player.y)
                        bullet.alive = False
                        settings.spacialGrid.removeClient(bullet.grid_id, bullet.x, bullet.y)
            
            # Player bullets vs enemy - only check alive bullets
        alive_player_bullets = [b for b in self.player.gun.bullets if b.alive]
        for bullet in alive_player_bullets:
            enemy_ids = settings.spacialGrid.getNearbyByType(bullet.x, bullet.y, "enemy")
            # print("nearby enemies: ",enemy_ids)
            for enemy_id in enemy_ids:
                enemy, _ = settings.spacialGrid.entity_registry[enemy_id]
                if bullet.gun_type_name == "rail":
                    if enemy.rect.colliderect(bullet.rect):  # Fast broad-phase
                        offset = (bullet.rect.x - enemy.rect.x, bullet.rect.y - enemy.rect.y)

                        enemy.health -= bullet.damage
                        self.sparks.append(Spark([enemy.x, enemy.y], math.radians(random.randint(0, 360)), random.randint(3, 6), (255, 255, 255), 3))
                        self.sparks.append(Spark([enemy.x, enemy.y], math.radians(random.randint(0, 360)), random.randint(3, 6), (255, 255, 255), 3))
                        self.sparks.append(Spark([enemy.x, enemy.y], math.radians(random.randint(0, 360)), random.randint(3, 6), (255, 255, 255), 3))
                        self.sparks.append(Spark([enemy.x, enemy.y], math.radians(random.randint(0, 360)), random.randint(3, 6), (255, 255, 255), 3))
                        self.sparks.append(Spark([enemy.x, enemy.y], math.radians(random.randint(0, 360)), random.randint(3, 6), (255, 255, 255), 3))
                        enemy.show_health_bar()  # Show health bar when hit
                        bullet.alive = False
                        settings.spacialGrid.removeClient(bullet.grid_id, bullet.x, bullet.y)
                        
                        if enemy.health <= 0:
                            self.sparks.append(Spark([enemy.x, enemy.y], math.radians(random.randint(0, 360)), random.randint(3, 6), enemy.image_average_color, 2))
                            self.sparks.append(Spark([enemy.x, enemy.y], math.radians(random.randint(0, 360)), random.randint(3, 6), enemy.image_average_color, 2))
                            self.sparks.append(Spark([enemy.x, enemy.y], math.radians(random.randint(0, 360)), random.randint(3, 6), enemy.image_average_color, 2))
                            self.sparks.append(Spark([enemy.x, enemy.y], math.radians(random.randint(0, 360)), random.randint(3, 6), enemy.image_average_color, 2))
                            self.sparks.append(Spark([enemy.x, enemy.y], math.radians(random.randint(0, 360)), random.randint(3, 6), enemy.image_average_color, 2))
                            self.sparks.append(Spark([enemy.x, enemy.y], math.radians(random.randint(0, 360)), random.randint(3, 6), enemy.image_average_color, 2))
                            self.sparks.append(Spark([enemy.x, enemy.y], math.radians(random.randint(0, 360)), random.randint(3, 6), enemy.image_average_color, 2))
                            self.sparks.append(Spark([enemy.x, enemy.y], math.radians(random.randint(0, 360)), random.randint(3, 6), enemy.image_average_color, 2))
                            self.sparks.append(Spark([enemy.x, enemy.y], math.radians(random.randint(0, 360)), random.randint(3, 6), enemy.image_average_color, 2))
                            self.sparks.append(Spark([enemy.x, enemy.y], math.radians(random.randint(0, 360)), random.randint(3, 6), enemy.image_average_color, 2))
                            self.sparks.append(Spark([enemy.x, enemy.y], math.radians(random.randint(0, 360)), random.randint(3, 6), enemy.image_average_color, 2))
                            self.sparks.append(Spark([enemy.x, enemy.y], math.radians(random.randint(0, 360)), random.randint(3, 6), enemy.image_average_color, 2))
                            self.sparks.append(Spark([enemy.x, enemy.y], math.radians(random.randint(0, 360)), random.randint(3, 6), enemy.image_average_color, 2))
                            self.sparks.append(Spark([enemy.x, enemy.y], math.radians(random.randint(0, 360)), random.randint(3, 6), enemy.image_average_color, 2))
                            self.sparks.append(Spark([enemy.x, enemy.y], math.radians(random.randint(0, 360)), random.randint(3, 6), enemy.image_average_color, 2))
                            enemy.alive = False
                            settings.spacialGrid.removeClient(enemy.grid_id, enemy.x, enemy.y)
                            

                        
                        break  # Bullet hit, no need to check more bullets
                else:

                    offset = (int(bullet.x - enemy.x), int(bullet.y - enemy.y))
                    enemy_mask = self.enemy_masks[self.enemy_type]
                    if enemy_mask.overlap(bullet.mask, offset):
                        enemy.health -= bullet.damage
                        self.sparks.append(Spark([enemy.x, enemy.y], math.radians(random.randint(0, 360)), random.randint(3, 6), (255, 255, 255), 3))
                        self.sparks.append(Spark([enemy.x, enemy.y], math.radians(random.randint(0, 360)), random.randint(3, 6), (255, 255, 255), 3))
                        self.sparks.append(Spark([enemy.x, enemy.y], math.radians(random.randint(0, 360)), random.randint(3, 6), (255, 255, 255), 3))
                        self.sparks.append(Spark([enemy.x, enemy.y], math.radians(random.randint(0, 360)), random.randint(3, 6), (255, 255, 255), 3))
                        self.sparks.append(Spark([enemy.x, enemy.y], math.radians(random.randint(0, 360)), random.randint(3, 6), (255, 255, 255), 3))
                        enemy.show_health_bar()  # Show health bar when hit
                        if bullet.penetration == 0 or bullet.hit_count == bullet.penetration:
                            bullet.alive = False
                            settings.spacialGrid.removeClient(bullet.grid_id, bullet.x, bullet.y)
                        else:
                            bullet.hit_count+=1

                        if enemy.health <= 0:
                            self.sparks.append(Spark([enemy.x, enemy.y], math.radians(random.randint(0, 360)), random.randint(3, 6), enemy.image_average_color, 2))
                            self.sparks.append(Spark([enemy.x, enemy.y], math.radians(random.randint(0, 360)), random.randint(3, 6), enemy.image_average_color, 2))
                            self.sparks.append(Spark([enemy.x, enemy.y], math.radians(random.randint(0, 360)), random.randint(3, 6), enemy.image_average_color, 2))
                            self.sparks.append(Spark([enemy.x, enemy.y], math.radians(random.randint(0, 360)), random.randint(3, 6), enemy.image_average_color, 2))
                            self.sparks.append(Spark([enemy.x, enemy.y], math.radians(random.randint(0, 360)), random.randint(3, 6), enemy.image_average_color, 2))
                            self.sparks.append(Spark([enemy.x, enemy.y], math.radians(random.randint(0, 360)), random.randint(3, 6), enemy.image_average_color, 2))
                            self.sparks.append(Spark([enemy.x, enemy.y], math.radians(random.randint(0, 360)), random.randint(3, 6), enemy.image_average_color, 2))
                            self.sparks.append(Spark([enemy.x, enemy.y], math.radians(random.randint(0, 360)), random.randint(3, 6), enemy.image_average_color, 2))
                            self.sparks.append(Spark([enemy.x, enemy.y], math.radians(random.randint(0, 360)), random.randint(3, 6), enemy.image_average_color, 2))
                            self.sparks.append(Spark([enemy.x, enemy.y], math.radians(random.randint(0, 360)), random.randint(3, 6), enemy.image_average_color, 2))
                            self.sparks.append(Spark([enemy.x, enemy.y], math.radians(random.randint(0, 360)), random.randint(3, 6), enemy.image_average_color, 2))
                            self.sparks.append(Spark([enemy.x, enemy.y], math.radians(random.randint(0, 360)), random.randint(3, 6), enemy.image_average_color, 2))
                            self.sparks.append(Spark([enemy.x, enemy.y], math.radians(random.randint(0, 360)), random.randint(3, 6), enemy.image_average_color, 2))
                            self.sparks.append(Spark([enemy.x, enemy.y], math.radians(random.randint(0, 360)), random.randint(3, 6), enemy.image_average_color, 2))
                            self.sparks.append(Spark([enemy.x, enemy.y], math.radians(random.randint(0, 360)), random.randint(3, 6), enemy.image_average_color, 2))
                            enemy.alive = False
                            settings.spacialGrid.removeClient(enemy.grid_id, enemy.x, enemy.y)

                        break  # Bullet hit, no need to check more bullets
        
    def spawn(self, screen):
        endX = random.randint(10, WINDOW_WIDTH-10)
        endY = random.randint(10, (WINDOW_HEIGHT/2)-10)
        enemy = Enemy(
            random.randint(10, WINDOW_WIDTH-10),
            random.randint(10, WINDOW_HEIGHT//3),
            20, self.dt*self.enemy_database[self.enemy_type]["speed"], self.player, endX, endY,
            self.enemy_database[self.enemy_type], 
            self.current_enemy_image
        )

        # Play boss theme if orbyprime is spawned
        if self.enemy_type == "orbyprime":
            pygame.mixer.music.load("./assets/sounds/bossthemeorbyprime.wav")
            pygame.mixer.music.set_volume(0.2)
            pygame.mixer.music.play(loops=-1)

        # settings.spacialGrid.addClient(enemy.grid_id, enemy.x, enemy.y)
        # Pass shared resources to avoid reloading
        enemy.gun.shared_sounds = self._shared_sounds
        enemy.gun.shared_bullet_images = self._shared_bullet_images
        self.enemies.append(enemy)