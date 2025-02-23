import pygame
import string
from utils import *
from globals import *

# setup pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("hyper typer")
clock = pygame.time.Clock()
running = True

# setup game objects
font = pygame.font.Font("freesansbold.ttf", 32) # PLACEHOLDER FONT
texts = ["hello people", "how are you", "this is a test",
          "goodbye", "thanks for playing", "this is the last text",
            "good job", "congratulations", "you did it", "you are a pro"]
typed = ""
score = 0
allowed_chars = allowed_chars = string.ascii_letters + string.digits + " "

from running_text import RunningTextManager

running_text_manager = RunningTextManager(
    texts=texts,
    max_texts_running=3,
    max_text_speed=5,
    font=font
)


# game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_BACKSPACE:
                if event.mod == pygame.KMOD_NONE:
                    typed = typed[:-1]
                elif event.mod == pygame.KMOD_LALT or event.mod == pygame.KMOD_LCTRL:
                    typed = ' '.join(typed.rstrip().split(' ')[:-1])
                elif event.mod == pygame.KMOD_LMETA:
                    typed = ''
            elif event.key == pygame.K_RETURN:
                if running_text_manager.remove_text_match(typed):
                    score += len(typed)
                typed = ''
            else:
                if event.unicode in allowed_chars:
                    typed += event.unicode
                
    screen.fill('black')

    # UPDATES GAME HERE
    running_text_manager.update()

    # RENDER GAME HERE
    running_text_manager.render(screen)

    draw_text(typed, 30, HEIGHT - 60, font, screen)
    draw_text(str(score), 30, 30, font, screen)

    # update the screen
    pygame.display.flip()
    clock.tick(60)

# quit pygame
pygame.quit()