import pygame

def draw_text(text, x, y, font, screen):
    '''
    Draw text on the screen at position x, y by converting the text to a surface and blitting it to the screen
    '''
    text = font.render(text, True, (255,255,255))
    screen.blit(text, (x, y))

def transparent_color(color, opacity):
    '''
    Get a color with a certain opacity by writing the color name
    '''
    c = pygame.color.Color(color)
    return c.r, c.g, c.b, opacity