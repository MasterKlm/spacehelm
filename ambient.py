import pygame, math


def create_light_surface(radius, color, reflectivity=0.5):
    light_surface = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)

    for y in range(radius*2):
        for x in range(radius*2):
            dx = x - radius
            dy = y - radius
            dist = math.sqrt(dx*dx + dy*dy)

            if dist < radius:
                # Linear falloff (bright in center, 0 at edge)
                attenuation = max(0, 1 - dist / radius)

                r = int(color[0] * reflectivity * attenuation)
                g = int(color[1] * reflectivity * attenuation)
                b = int(color[2] * reflectivity * attenuation)
                a = int(255 *  reflectivity * attenuation)

                light_surface.set_at((x, y), (r, g, b, a))

    return light_surface
