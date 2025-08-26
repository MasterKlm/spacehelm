import pygame
from settings import *
from player import *
import math
from spawner import *
from level import Level
from timer import Timer

pygame.init()

font = pygame.font.Font(None, 30)

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

# Hide the default mouse cursor
pygame.mouse.set_visible(False)

# Load and setup custom cursor
cursor_image = pygame.image.load('./assets/crosshair.png').convert_alpha()  # Replace with your cursor image
cursor_image = pygame.transform.scale(cursor_image, (100, 100))  # Adjust size as needed
cursor_rect = cursor_image.get_rect()

player_jet_image = pygame.image.load('./assets/jet.png').convert_alpha()
player_jet_image = pygame.transform.scale(player_jet_image, (40, 40))
pygame.mixer.music.load("./assets/soothing.wav")
pygame.mixer.music.play(loops=-1)

delta_time = 0.1
player = Player(WINDOW_WIDTH/2, WINDOW_HEIGHT/1.4, 50, (0, 0), player_jet_image, delta_time)

levels = [
    Level([Spawner(2, delta_time, player, 1000), Spawner(10, delta_time, player, 2000)]), 
    Level([Spawner(3, delta_time, player, 100)])
]

level_index = 0

# Level transition variables
level_transition_timer = Timer(5000)  # 5 seconds in milliseconds
waiting_for_next_level = False
level_completed = False

# Track mouse position
mouse_pos = (0, 0)

while True:
    screen.fill((0, 0, 0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        if event.type == pygame.MOUSEMOTION:
            mouse_pos = event.pos
            player.mos_pos = mouse_pos
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Only allow shooting if not in transition
            if not waiting_for_next_level:
                player.gun.shoot()
    
    delta_time = clock.tick(60)
    delta_time = max(0.001, min(0.1, delta_time))
    player.dt = delta_time

    # Handle level transitions
    if level_index < len(levels):
        current_level = levels[level_index]
        
        # Check if current level is complete
        if current_level.complete and not waiting_for_next_level and not level_completed:
            # Level just completed, start transition timer
            level_completed = True
            waiting_for_next_level = True
            level_transition_timer.activate()
        
        # Update transition timer
        if waiting_for_next_level:
            level_transition_timer.update()
            
            # Check if transition is complete
            if not level_transition_timer.active:
                # Move to next level
                level_index += 1
                waiting_for_next_level = False
                level_completed = False

    # Update spawner delta time
    if level_index < len(levels) and not waiting_for_next_level:
        current_level = levels[level_index]
        for spawner in current_level.spawners:
            spawner.dt = delta_time

    # Display UI
    fps_text = font.render(f"fps: {clock.get_fps():.2f}", True, (255, 255, 255))
    health_text = font.render(f"Health: {0 if player.health < 0 else player.health}", True, (0, 255, 0))
    level_text = font.render(f"Level: {level_index + 1}", True, (255, 255, 255))

    screen.blit(fps_text, (10, 10))
    screen.blit(health_text, (20, WINDOW_HEIGHT - 60))
    screen.blit(level_text, (10, 40))
    
    # Game over check
    if player.health < 0:
        game_over_font = pygame.font.Font(None, 60)
        game_over_text = game_over_font.render("Game Over", True, (255, 0, 0))
        screen.blit(game_over_text, (WINDOW_WIDTH/2.8, WINDOW_HEIGHT/2))
    
    # All levels completed
    elif level_index >= len(levels):
        victory_font = pygame.font.Font(None, 60)
        victory_text = victory_font.render("Victory! All Levels Complete!", True, (0, 255, 0))
        screen.blit(victory_text, (WINDOW_WIDTH/2 - 300, WINDOW_HEIGHT/2))
    
    # Level transition screen
    elif waiting_for_next_level:
        transition_font = pygame.font.Font(None, 50)
        next_level_text = transition_font.render(f"Level {level_index + 1} Complete!", True, (255, 255, 0))
        
        # Calculate remaining time
        remaining_time = max(0, (level_transition_timer.duration - (pygame.time.get_ticks() - level_transition_timer.start_time)) / 1000)
        countdown_text = font.render(f"Next level in: {remaining_time:.1f}s", True, (255, 255, 255))
        
        screen.blit(next_level_text, (WINDOW_WIDTH/2 - 100, WINDOW_HEIGHT/2 - 50))
        screen.blit(countdown_text, (WINDOW_WIDTH/2 - 100, WINDOW_HEIGHT/2 + 20))
        
        # Still update player but don't update level
        player.update(screen)
    
    # Normal gameplay
    else:
        player.update(screen)
        if level_index < len(levels):
            levels[level_index].update(screen)
    
    # Draw custom cursor at mouse position (do this last so it's on top)
    cursor_rect.center = mouse_pos
    screen.blit(cursor_image, cursor_rect)
    
    pygame.display.flip()