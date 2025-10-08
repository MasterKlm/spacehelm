import pygame
import settings
from player import *
import math
from spawner import *
from level import Level
from timer import Timer
import random
from resourcemanager import ResourceManager
from spacialgrid import SpatialGrid
from customtkinter import *
from tkinter import font as tkfont
import os

# Load custom font for Windows
font_path = os.path.abspath("./assets/fonts/PixelifySans-Regular.ttf")

if os.name == 'nt':
    import ctypes
    from ctypes import wintypes
    FR_PRIVATE = 0x10
    gdi32 = ctypes.WinDLL('gdi32', use_last_error=True)
    gdi32.AddFontResourceExW.argtypes = [wintypes.LPCWSTR, wintypes.DWORD, wintypes.LPVOID]
    gdi32.AddFontResourceExW(font_path, FR_PRIVATE, 0)

# Initialize pygame once at startup
pygame.init()

def show_menu():
    """Display the main menu and wait for user action"""
    global menu_choice
    menu_choice = None
    
    app = CTk()
    app.geometry("1000x500")
    set_appearance_mode("dark")
    app.title("Spacehelm")
    
    def start_game():
        global menu_choice
        menu_choice = "start"
        app.destroy()
    
    def exit_game(event=None):
        global menu_choice
        menu_choice = "exit"
        app.destroy()
    
    # Create UI elements
    custom_font = CTkFont(family="Pixelify Sans", size=70)
    custom_button_font = CTkFont(family="Pixelify Sans", size=15)
    
    label = CTkLabel(app, width=100, height=100, text="SpaceHelm", 
                     text_color="#32A956", font=custom_font)
    label.pack(pady=100)
    
    button = CTkButton(app, width=100, height=30, text="Start game", 
                       font=custom_button_font, fg_color="#32A956", 
                       text_color="#ffffff", command=start_game)
    button.pack(pady=2)
    
    app.bind("<Escape>", exit_game)
    app.protocol("WM_DELETE_WINDOW", exit_game)  # Handle window close button
    
    app.mainloop()
    
    return menu_choice

def run_pygame():
    """Run the main pygame game loop"""
    screen = pygame.display.set_mode((settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT))
    pygame.display.set_caption("Spacehelm")
    
    font = pygame.font.Font("./assets/fonts/PixelifySans-Regular.ttf", 30)

    settings.mainResManager = ResourceManager()
    settings.spacialGrid = SpatialGrid(100)
    
    clock = pygame.time.Clock()

    # Hide the default mouse cursor
    pygame.mouse.set_visible(False)

    # Load and setup custom cursor
    cursor_image = pygame.image.load('./assets/images/crosshair.png').convert_alpha()
    cursor_image = pygame.transform.scale(cursor_image, (100, 100))
    cursor_rect = cursor_image.get_rect()

    player_jet_image = pygame.image.load('./assets/images/jet.png').convert_alpha()
    player_jet_image = pygame.transform.scale(player_jet_image, (40, 40))
    
    pygame.mixer.music.load("./assets/sounds/soothing.wav")
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(loops=-1)

    delta_time = 0.1
    player = Player(settings.WINDOW_WIDTH/2, settings.WINDOW_HEIGHT/1.4, 50, (0, 0), player_jet_image, delta_time)

    levels = [
        # Level([[Spawner(1, delta_time, player, 100)]]),

        #load testing:
        # Level([[Spawner(100, delta_time, player, 80), Spawner(200, delta_time, player, 200, "orby")]]),


        Level([[Spawner(5, delta_time, player, 100)]]),
        Level([[Spawner(10, delta_time, player, 80), Spawner(3, delta_time, player, 200, "orby")]]),
        Level([[Spawner(8, delta_time, player, 100, "orby"), Spawner(12, delta_time, player, 120)]]),
        Level([[Spawner(15, delta_time, player, 70), Spawner(5, delta_time, player, 500, "orby")]]),
        Level([[Spawner(20, delta_time, player, 60), Spawner(10, delta_time, player, 400, "orby")]]),
        Level([[Spawner(25, delta_time, player, 50), Spawner(15, delta_time, player, 350, "orby")]]),
        Level([[Spawner(30, delta_time, player, 45), Spawner(20, delta_time, player, 300, "orby")]]),
        Level([[Spawner(35, delta_time, player, 40), Spawner(25, delta_time, player, 250, "orby")]]),
        Level([[Spawner(40, delta_time, player, 35), Spawner(30, delta_time, player, 200, "orby")]]),
        Level([[Spawner(50, delta_time, player, 30), Spawner(40, delta_time, player, 150, "orby")]]),
        Level([[Spawner(1, delta_time, player, 100, "orbyprime")]]),
    ]
    
    level_index = 0

    # Level transition variables
    level_transition_timer = Timer(5000)
    waiting_for_next_level = False
    level_completed = False

    # Track mouse position
    mouse_pos = (0, 0)

    backdrop_star_array = []
    star_count = 80

    for i in range(star_count):
        backdrop_star_array.append({
            "x": random.randint(5, settings.WINDOW_WIDTH),
            "y": random.randint(5, settings.WINDOW_HEIGHT)
        })

    settings.running = True
    while settings.running:
        screen.fill((0, 0, 0))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                settings.running = False
                
            if event.type == pygame.MOUSEMOTION:
                mouse_pos = event.pos
                player.mos_pos = mouse_pos
                
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if not waiting_for_next_level:
                    player.gun.shoot()
                    
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                if not waiting_for_next_level and player.teleporter_timer.active == False:
                    mouse_pos = event.pos
                    player.x = mouse_pos[0]
                    player.y = mouse_pos[1]
                    
                    # Create teleport sparks
                    for _ in range(15):
                        player.sparks.append(
                            Spark([player.x, player.y], 
                                  math.radians(random.randint(0, 360)), 
                                  random.randint(3, 6),
                                  (173, 216, 230), 2)
                        )
                    player.teleporter_timer.activate()
        
        delta_time = clock.tick(settings.FPS)
        delta_time = max(0.001, min(0.1, delta_time))
        player.dt = delta_time
        
        # Manage backdrop stars
        if len(backdrop_star_array) < star_count:
            backdrop_star_array.append({
                "x": random.randint(5, settings.WINDOW_WIDTH),
                "y": random.randint(5, settings.WINDOW_HEIGHT)
            })

        for star in backdrop_star_array[:]:  # Use slice to avoid modification during iteration
            if star["y"] < settings.WINDOW_HEIGHT:
                star["y"] += 1
                pygame.draw.rect(screen, (255, 255, 255), (star["x"], star["y"], 3, 3))
            else:
                backdrop_star_array.remove(star)

        # Handle level transitions
        if level_index < len(levels):
            current_level = levels[level_index]
            
            if current_level.complete and not waiting_for_next_level and not level_completed:
                level_completed = True
                waiting_for_next_level = True
                level_transition_timer.activate()
            
            if waiting_for_next_level:
                level_transition_timer.update()
                
                if not level_transition_timer.active:
                    level_index += 1
                    waiting_for_next_level = False
                    level_completed = False

        # Update spawner delta time
        if level_index < len(levels) and not waiting_for_next_level:
            current_level = levels[level_index]
            for spawner in current_level.spawners:
                if type(spawner) == list:
                    for s in spawner:
                        s.dt = delta_time
                else:
                    spawner.dt = delta_time

        # Display UI
        fps_text = font.render(f"fps: {clock.get_fps():.2f}", True, (255, 255, 255))
        health_text = font.render(f"Health: {0 if player.health < 0 else player.health}", True, (0, 255, 0))
        level_text = font.render(f"Level: {level_index + 1}", True, (255, 255, 255))

        screen.blit(fps_text, (10, 10))
        screen.blit(health_text, (20, settings.WINDOW_HEIGHT - 80))
        screen.blit(level_text, (10, 40))
        
        gun_index_font = pygame.font.Font("./assets/fonts/PixelifySans-Regular.ttf", 40)
        gun_index_text = gun_index_font.render(
            player.gun_data[str(player.gun_index)]["gun_type"], 
            True, 
            player.gun_data[str(player.gun_index)]["gun_type_text_color"]
        )
        screen.blit(gun_index_text, ((settings.WINDOW_WIDTH/2) - 30, settings.WINDOW_HEIGHT - 80))
        
        # Game over check
        if player.health <= 0:
            game_over_font = pygame.font.Font("./assets/fonts/PixelifySans-Regular.ttf", 60)
            game_over_text = game_over_font.render("Game Over", True, (255, 0, 0))
            
            screen.blit(game_over_text, (settings.WINDOW_WIDTH/2.8, settings.WINDOW_HEIGHT/2))
        
        # All levels completed
        elif level_index >= len(levels):
            victory_font = pygame.font.Font("./assets/fonts/PixelifySans-Regular.ttf", 60)
            victory_text = victory_font.render("Victory! All Levels Complete!", True, (0, 255, 0))
            victory_rect = victory_text.get_rect(center=(settings.WINDOW_WIDTH // 2, settings.WINDOW_HEIGHT // 2))
            screen.blit(victory_text, victory_rect)
        
        # Level transition screen
        elif waiting_for_next_level:
            transition_font = pygame.font.Font("./assets/fonts/PixelifySans-Regular.ttf", 50)
            next_level_text = transition_font.render(f"Level {level_index + 1} Complete!", True, (255, 255, 0))
            next_level_rect = next_level_text.get_rect(center=(settings.WINDOW_WIDTH // 2, settings.WINDOW_HEIGHT // 2 - 40))

            remaining_time = max(0, (level_transition_timer.duration - (pygame.time.get_ticks() - level_transition_timer.start_time)) / 1000)
            countdown_text = font.render(f"Next level in: {remaining_time:.1f}s", True, (255, 255, 255))
            countdown_rect = countdown_text.get_rect(center=(settings.WINDOW_WIDTH // 2, settings.WINDOW_HEIGHT // 2 + 30))

            screen.blit(next_level_text, next_level_rect)
            screen.blit(countdown_text, countdown_rect)

            player.update(screen)
        
        # Normal gameplay
        else:
            player.update(screen)
            if level_index < len(levels):
                levels[level_index].update(screen)
        
        # Draw custom cursor at mouse position
        cursor_rect.center = mouse_pos
        screen.blit(cursor_image, cursor_rect)
        
        pygame.display.flip()
    
    # Clean up pygame display
    pygame.display.quit()
    pygame.mixer.music.stop()

def main():
    """Main game loop - alternates between menu and game"""
    while True:
        choice = show_menu()
        
        if choice == "start":
            run_pygame()
        else:
            # User chose to exit
            break
    
    # Clean up and exit
    pygame.quit()

if __name__ == "__main__":
    main()