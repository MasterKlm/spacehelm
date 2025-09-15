import pygame
from settings import *

class Level:
    def __init__(self, spawners):
        self.spawners = spawners
        self.current_spawner_index = 0
        self.complete = False
    
    def update(self, screen):
        # Check if we've completed all spawner groups
        if self.current_spawner_index >= len(self.spawners):
            self.complete = True
            return
        
        # Get the current spawner (could be single spawner or list of spawners)
        current_spawner_group = self.spawners[self.current_spawner_index]
        
        # Handle list of spawners (simultaneous spawning)
        if isinstance(current_spawner_group, list):
            all_spawners_complete = True
            
            # Update all spawners in the group
            for spawner in current_spawner_group:
                spawner.update(screen)
                
                # Check if this spawner is not complete yet
                if not (spawner.done_spawning and len(spawner.enemies) == 0):
                    all_spawners_complete = False
            
            # If all spawners in the group are complete, move to next group
            if all_spawners_complete:
                self.current_spawner_index += 1
        
        # Handle single spawner
        else:
            current_spawner_group.update(screen)
            
            # Check if spawner is complete (done spawning AND all enemies defeated)
            if current_spawner_group.done_spawning and len(current_spawner_group.enemies) == 0:
                self.current_spawner_index += 1
    
    def get_current_spawners(self):
        """Returns the currently active spawner(s), or None if level is complete"""
        if self.current_spawner_index < len(self.spawners):
            current = self.spawners[self.current_spawner_index]
            # Always return as list for consistency
            return current if isinstance(current, list) else [current]
        return None
    
    def get_current_spawner(self):
        """Legacy method for backward compatibility - returns first spawner only"""
        current_spawners = self.get_current_spawners()
        return current_spawners[0] if current_spawners else None