import pygame
import string
import os
from utils import *
from globals import *

from text import FormattedText, TextInfo
from text_managers import RunningTextManager

# setup pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("hyper typer")
clock = pygame.time.Clock()
running = True

# setup game objects
# get font from the assets folder
font_path = os.path.join(BASE_DIR, 'assets', 'fonts', 'anonymouspro.ttf')
font = pygame.font.Font(font_path, 32)

typed = ""
score = 0
allowed_chars = allowed_chars = string.ascii_letters + string.digits + " " + ",.?\"!@#$%^&*()"

texts = [
    "hello people how are you this is a test goodbye and thanks for playing you did it you are a pro",
    "no seriously who thought this would be a good idea",
    "this game is kinda trash, nobody would want to play a game you just type and type and type..."
]
text_info = TextInfo(font, 'white', 'red', 'green', 'yellow', 30, 10, 0)
running_text_manager = RunningTextManager(texts, text_info, -2, 4)

# game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_BACKSPACE:
                if event.mod == pygame.KMOD_NONE:
                    typed = typed[:-1]
                    running_text_manager.total_typed -= 1

                # remove the last word
                elif event.mod == pygame.KMOD_LALT or event.mod == pygame.KMOD_LCTRL:
                    typed = ' '.join(typed.rstrip().split(' ')[:-1])
                # remove the entire typed text, only works for mac (LMETA is the command key on mac)
                elif event.mod == pygame.KMOD_LMETA:
                    typed = ''
            elif event.key == pygame.K_RETURN:
                typed = ''
            elif event.key == pygame.K_LMETA:
                running_text_manager.change_selected_text(+1)
            elif event.key == pygame.K_RMETA:
                running_text_manager.change_selected_text(-1)
            else:
                if event.unicode in allowed_chars: 
                    typed += event.unicode
                    running_text_manager.total_typed += 1
            
            running_text_manager.update_typing(typed)
                
    
    screen.fill(pygame.color.Color(33, 51, 45))

    # UPDATES GAME HERE
    running_text_manager.update()

    # RENDER GAME HERE
    running_text_manager.render(screen)

    # update the screen
    pygame.display.flip()
    clock.tick(60)

# quit pygame
pygame.quit()