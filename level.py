import pygame
from settings import *

class Level:
    def __init__(self, spawners):
        self.spawners = spawners
        self.current_spawner_index = 0
        self.complete = False
        # self.font = pygame.font.Font(None, 60)
    def update(self, screen):
        # Check if we've completed all spawners
        if self.current_spawner_index >= len(self.spawners):
            # level_complete_text = self.font.render(f"Level Complete ", True, (0,255,0))
            # screen.blit(level_complete_text, (WINDOW_WIDTH/2.8, WINDOW_HEIGHT/2))
            self.complete = True
            return
        
        # Get the current spawner
        current_spawner = self.spawners[self.current_spawner_index]
        
        # Update the current spawner
        current_spawner.update(screen)
        
        # Check if current spawner is done spawning AND all enemies are defeated
        if current_spawner.done_spawning and len(current_spawner.enemies) == 0:
            # Move to next spawner
            self.current_spawner_index += 1
            
            # Check if we've completed all spawners
            if self.current_spawner_index >= len(self.spawners):
                self.complete = True
    
    def get_current_spawner(self):
        """Returns the currently active spawner, or None if level is complete"""
        if self.current_spawner_index < len(self.spawners):
            return self.spawners[self.current_spawner_index]
        return None