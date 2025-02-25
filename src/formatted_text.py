from globals import WIDTH, HEIGHT
import pygame
from utils import transparent_color

class FormattedText:
    '''Format text to be displayed with a left align and a max number of letters per line'''
    def __init__(self, text, font, text_color, wrong_color, right_color, corrected_color, line_max_letters):
        self.text = text
        self.font = font
        self.colors = {
            'default': text_color,
            'wrong': wrong_color,
            'correct': right_color,
            'corrected': corrected_color
        }

        # Split the text into lines based on the max number of letters per line
        self.char_status = ['default'] * len(text)
        self.lines = []
        cur_line = ''
        words = text.split(' ')

        for i in range(len(words)):
            if len(cur_line) + len(words[i]) < line_max_letters:
                cur_line += words[i] + ' '
            elif len(cur_line) + len(words[i]) >= line_max_letters:
                self.lines.append(cur_line)
                cur_line = words[i] + ' '
            
            if i == len(words) -1:
                self.lines.append(cur_line.rstrip())

        # positions and sizes
        self.char_width, self.char_height = font.size('A')
        self.letter_spacing = 0
        self.line_distance = 10
        self.x = WIDTH/2 - line_max_letters * self.char_width / 2
        self.y = HEIGHT/2 - self.char_height * len(self.lines) / 2

        self.underline_render = self.font.render('_', True, 'white')
        self.underline_pos = (self.x, self.y + 2)
        self.cur_line = 0
        
        self.wpm = 0
        self.timer = 0
        self.seconds = 0
        self.accuracy = 100

        # self.rect_surface = pygame.Surface((self.char_width, self.char_height))
        # self.rect_surface.set_alpha(50)
        
    def update_timer(self):
        self.timer += 1
        if self.timer >= 60:
            self.timer = 0
            self.seconds += 1
    
    def update(self, typed):
        '''Update all the information of the text, like the status of each character, the current line typed length and the underline position'''
        for i in range(len(typed)):
            if self.text[i] == typed[i]:
                if self.char_status[i] == 'wrong' or self.char_status[i] == 'corrected':
                    self.char_status[i] = 'corrected'
                else:
                    self.char_status[i] = 'correct'
            else:
                self.char_status[i] = 'wrong'

        # getting the total typed in the current line
        amount_typed_inline = len(typed)
        for i in range(len(self.lines)):
            line = self.lines[i]
            if amount_typed_inline + 1 > len(line):
                amount_typed_inline -= len(line)
            else:
                self.cur_line = i
                break

        self.underline_pos = (
            self.x + self.char_width * amount_typed_inline + amount_typed_inline * self.letter_spacing,                   
            self.y + self.char_height * self.cur_line + self.cur_line * self.line_distance + 2
        )

        self.accuracy = round(100 - 100 * (self.char_status.count('wrong') / len(self.text)))
        self.wpm = round(len(typed) / 5) * 60 // (self.seconds + 1)

    def render(self, screen):
        '''Render each individual character with it's status color, into the screen'''

        # tracking by id was used because each line has it's own width size, thus you can't calculate where you are
        status_id = 0
        for i in range(len(self.lines)):
            line = self.lines[i]
            for j in range(len(line)):
                char = line[j]
                color = self.colors[self.char_status[status_id]]
                char_render = self.font.render(char, True, color)
                char_y = self.y + self.char_height * i + i * self.line_distance
                char_x = self.x + self.char_width * j + j * self.letter_spacing
                
                # ADDS BACKGROND COLOR TO THE CHARACTERS BASED ON THE CHAR STATUS
                # if self.char_status[status_id] != 'default':
                #     self.rect_surface.fill(color)
                #     screen.blit(self.rect_surface, (char_x, char_y))

                screen.blit(char_render, (char_x, char_y))
                status_id += 1

        screen.blit(self.underline_render, self.underline_pos)

        accuracy_text = self.font.render('Accuracy: ' + str(self.accuracy) + '%', True, 'white')
        screen.blit(accuracy_text, (WIDTH - 250, 50))

        wpm_render = self.font.render('WPM: ' + str(self.wpm), True, 'white')
        screen.blit(wpm_render, (50, 50))