import pygame

def get_average_color(surface):
    arr = pygame.surfarray.pixels3d(surface)
    if surface.get_masks()[3] != 0:  # Has alpha
        alpha = pygame.surfarray.pixels_alpha(surface)
        mask = alpha > 0
        if mask.any():
            r = arr[:,:,0][mask].mean()
            g = arr[:,:,1][mask].mean()
            b = arr[:,:,2][mask].mean()
        else:
            r = g = b = 0
    else:
        r = arr[:,:,0].mean()
        g = arr[:,:,1].mean()
        b = arr[:,:,2].mean()
    return (int(r), int(g), int(b))