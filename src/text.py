import pygame
from globals import WIDTH, HEIGHT

class TextInfo:
    def __init__(self, font, text_color, wrong_color, right_color, corrected_color, line_max_letters, line_distance, letter_spacing):
        self.font = font
        self.text_color = text_color
        self.wrong_color = wrong_color
        self.right_color = right_color
        self.corrected_color = corrected_color
        self.line_max_letters = line_max_letters
        self.line_distance = line_distance
        self.letter_spacing = letter_spacing


class FormattedText:
    '''Format text to be displayed with a left align and a max number of letters per line'''
    def __init__(self, text, text_info):
        self.typed = ''
        self.text = text
        self.font = text_info.font
        self.colors = {
            'default': text_info.text_color,
            'wrong': text_info.wrong_color,
            'correct': text_info.right_color,
            'corrected': text_info.corrected_color
        }

        # Split the text into lines based on the max number of letters per line
        self.char_status = ['default'] * len(text)
        self.lines = []
        cur_line = ''
        words = text.split(' ')
        self.max_chars_inline = 0

        for i in range(len(words)):
            if len(cur_line) + len(words[i]) < text_info.line_max_letters:
                cur_line += words[i] + ' '
            elif len(cur_line) + len(words[i]) >= text_info.line_max_letters:
                self.lines.append(cur_line)
                cur_line = words[i] + ' '
            
            if i == len(words) -1:
                self.lines.append(cur_line.rstrip())

            if len(cur_line) > self.max_chars_inline:
                    self.max_chars_inline = len(cur_line)

        # positions, spacing and movement
        self.char_width, self.char_height = text_info.font.size('A')
        self.letter_spacing = text_info.letter_spacing
        self.line_distance = text_info.line_distance

        # position and speed
        self.x = WIDTH/2 - text_info.line_max_letters * self.char_width / 2
        self.y = HEIGHT/2 - self.char_height * len(self.lines) / 2
        self.x_speed = 0
        self.y_speed = 0

        # underline position and render
        self.underline_render = self.font.render('_', True, 'white')
        self.underline_pos = (self.x, self.y + 2)
        self.amount_typed_inline = 0
        self.cur_line = 0
        self.cur_char_n = 0
        self.underline_bottom_distance = 2

        # selected rectangle
        self.selected_border_size = 3
        self.selected_padding = 20

        # BACKGROUND COLORS FOR EACH CHARACTER
        # self.rect_surface = pygame.Surface((self.char_width, self.char_height))
        # self.rect_surface.set_alpha(50)
    
    def update_typed_inline(self):
        amount_typed_inline = len(self.typed)
        for i in range(len(self.lines)):
            line = self.lines[i]
            if amount_typed_inline + 1 > len(line):
                amount_typed_inline -= len(line)
            else:
                self.cur_line = i
                break
        self.amount_typed_inline = amount_typed_inline
    
    def type_new_char(self, new_char):
        '''Update all the information of the text, like the status of each character, the current line self.typed length and the underline position'''
        self.typed += new_char
        
        for i in range(len(self.typed)):
            if self.text[i] == self.typed[i]:
                if self.char_status[i] == 'wrong' or self.char_status[i] == 'corrected':
                    self.char_status[i] = 'corrected'
                else:
                    self.char_status[i] = 'correct'
            else:
                self.char_status[i] = 'wrong'
    
    def remove_last_char(self):
        if self.typed:
            char = self.typed[-1]
            self.typed = self.typed[:-1]
            return char

    def remove_last_word(self):
        if self.typed:
            last_word = self.typed.rstrip().split(' ')[-1]
            self.typed = ' '.join(self.typed.rstrip().split(' ')[:-1])
            return last_word

    def remove_whole_text(self):
        if self.typed:
            text = self.typed
            self.typed = ''
            return text

    def update(self):
        self.x += self.x_speed
        self.y += self.y_speed
        
        self.underline_pos = (
            ((self.x + self.char_width * self.amount_typed_inline) + (self.amount_typed_inline * self.letter_spacing)) - self.x_speed,                   
            ((self.y + self.char_height * self.cur_line) + (self.cur_line * self.line_distance) + self.underline_bottom_distance) - self.y_speed
        )

        self.update_typed_inline()
        self.cur_char_n = len(self.typed)-1

    def render(self, screen):
        '''Render each individual character with it's status color, into the screen'''

        # tracking by id was used because each line has it's own width size, thus you can't calculate where you are
        status_id = 0
        for i in range(len(self.lines)):
            line = self.lines[i]
            for j in range(len(line)):
                char = line[j]
                color = self.colors['default'] if status_id > self.cur_char_n else self.colors[self.char_status[status_id]]
                char_render = self.font.render(char, True, color)
                char_y = self.y + self.char_height * i + i * self.line_distance
                char_x = self.x + self.char_width * j + j * self.letter_spacing
                
                # BACKGROUND COLORS FOR EACH CHARACTER
                # if self.char_status[status_id] != 'default':
                #     self.rect_surface.fill(color)
                #     screen.blit(self.rect_surface, (char_x, char_y))

                screen.blit(char_render, (char_x, char_y))
                status_id += 1

        screen.blit(self.underline_render, self.underline_pos)

    def render_rectangle_around_selected(self, screen):
        '''Render a rectangle around the selected text'''
        x = self.x - self.selected_padding
        y = self.y - self.selected_padding + 5
        width = (self.max_chars_inline * self.char_width) + self.selected_padding
        height = ((len(self.lines) + 1) * self.char_height) + self.selected_padding + 10

        white_rect = pygame.Rect(x, y, width, height)
        inside_rect = pygame.Rect(x+self.selected_border_size, y+self.selected_border_size, width-self.selected_border_size*2, height-self.selected_border_size*2)

        pygame.draw.rect(screen, 'white', white_rect)
        pygame.draw.rect(screen, pygame.color.Color(33, 51, 45), inside_rect)