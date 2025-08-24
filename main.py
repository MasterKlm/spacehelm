import pygame
from settings import *
from player import *
import math
from spawner import *

pygame.init()

font = pygame.font.Font(None, 30)

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()
player_jet_image = pygame.image.load('./assets/jet.png').convert_alpha()
player_jet_image = pygame.transform.scale(player_jet_image, (40,40))
pygame.mixer.music.load("./assets/soothing.wav")
pygame.mixer.music.play(loops=-1)
delta_time = 0.1
player = Player(WINDOW_WIDTH/2, WINDOW_HEIGHT/1.4, 50, (0,0), player_jet_image, delta_time)
spawner = Spawner(10, delta_time, player)
while True:
    screen.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        if event.type == pygame.MOUSEMOTION:
            mos_pos = event.pos
            player.mos_pos = mos_pos
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            player.shoot()
    delta_time = clock.tick(60)
    delta_time = max(0.001, min(0.1, delta_time))
    player.dt = delta_time
    spawner.dt = delta_time

    fps_text = font.render(f"fps: {clock.get_fps():.2f}", True, (255,255,255))
    health_text = font.render(f"Health: {0 if player.health<0 else player.health}", True, (0,255,0))

    screen.blit(fps_text, (10, 10))
    screen.blit(health_text, (20, WINDOW_HEIGHT-60))
    if player.health<0:
        game_over_font = pygame.font.Font(None, 60)
        game_over_text = game_over_font.render("Game Over", True, (255, 0,0))
        screen.blit(game_over_text, (WINDOW_WIDTH/2.5, WINDOW_HEIGHT/2))
        pass
    else:
        player.update(screen)
        spawner.update(screen)
    pygame.display.flip()
