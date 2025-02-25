import pygame
import string
import os
from utils import *
from globals import *

from running_text import RunningTextManager
from formatted_text import FormattedText

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
allowed_chars = allowed_chars = string.ascii_letters + string.digits + " "

text = "hello people how are you this is a test goodbye and thanks for playing this is the last text good job congratulations you did it you are a pro"
formatted_text = FormattedText(text, font, 'white', 'red', 'green', 'yellow', 30)


texts = ["hello people", "how are you", "this is a test",
          "goodbye", "thanks for playing", "this is the last text",
            "good job", "congratulations", "you did it", "you are a pro"]
running_text_manager = RunningTextManager(
    texts=texts,
    max_texts_running=3,
    max_text_speed=5,
    max_text_spawn_delay=4,
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

                # remove the last word
                elif event.mod == pygame.KMOD_LALT or event.mod == pygame.KMOD_LCTRL:
                    typed = ' '.join(typed.rstrip().split(' ')[:-1])
                # remove the entire typed text, only works for mac (LMETA is the command key on mac)
                elif event.mod == pygame.KMOD_LMETA:
                    typed = ''
            elif event.key == pygame.K_RETURN:
                if running_text_manager.remove_text_match(typed):
                    score += len(typed)
                typed = ''
            else:
                if event.unicode in allowed_chars: 
                    typed += event.unicode
            
            formatted_text.update(typed)
                
    
    screen.fill(pygame.color.Color(33, 51, 45))

    # UPDATES GAME HERE
    formatted_text.update_timer()

    # RENDER GAME HERE
    formatted_text.render(screen)

    # update the screen
    pygame.display.flip()
    clock.tick(60)

# quit pygame
pygame.quit()