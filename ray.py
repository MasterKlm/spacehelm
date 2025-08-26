from settings import *
import pygame
import math

class Ray:
    def __init__(self, start_x, start_y, end_x, end_y, color=(255, 0, 0)):
        self.start_x = start_x
        self.start_y = start_y
        self.color = color
        
        # Calculate direction vector
        dx = end_x - start_x
        dy = end_y - start_y
        
        # Extend the ray to the window edge
        self.end_x, self.end_y = self.calculate_window_intersection(start_x, start_y, dx, dy)
        
        self.angle = math.atan2(dy, dx)
    
    def calculate_window_intersection(self, start_x, start_y, dx, dy):
        """Calculate where the ray intersects with window boundaries"""
        # If direction is zero, return current position
        if dx == 0 and dy == 0:
            return start_x, start_y
        
        # Calculate intersection with each window edge
        intersections = []
        
        # Right edge (x = WINDOW_WIDTH)
        if dx > 0:
            t = (WINDOW_WIDTH - start_x) / dx
            y_intersect = start_y + t * dy
            if 0 <= y_intersect <= WINDOW_HEIGHT:
                intersections.append((WINDOW_WIDTH, y_intersect))
        
        # Left edge (x = 0)
        if dx < 0:
            t = -start_x / dx
            y_intersect = start_y + t * dy
            if 0 <= y_intersect <= WINDOW_HEIGHT:
                intersections.append((0, y_intersect))
        
        # Bottom edge (y = WINDOW_HEIGHT)
        if dy > 0:
            t = (WINDOW_HEIGHT - start_y) / dy
            x_intersect = start_x + t * dx
            if 0 <= x_intersect <= WINDOW_WIDTH:
                intersections.append((x_intersect, WINDOW_HEIGHT))
        
        # Top edge (y = 0)
        if dy < 0:
            t = -start_y / dy
            x_intersect = start_x + t * dx
            if 0 <= x_intersect <= WINDOW_WIDTH:
                intersections.append((x_intersect, 0))
        
        # Return the closest intersection
        if intersections:
            closest = min(intersections, 
                         key=lambda p: (p[0] - start_x)**2 + (p[1] - start_y)**2)
            return closest
        
        # Fallback - shouldn't happen if start is inside window
        return start_x + dx, start_y + dy
    
    def update(self, screen):
        self.angle = math.atan2((self.end_y - self.start_y), (self.end_x - self.start_x))
    
    def render(self, screen):
        pygame.draw.line(screen, self.color, (self.start_x, self.start_y), (self.end_x, self.end_y))