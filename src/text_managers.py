from text import FormattedText
import random
from text import FormattedText
from globals import WIDTH

class StaticTextManager:
    def __init__(self, texts, text_info, time_seconds):
        self.remaining_texts = []
        self.current_text = ''
        self.timer = 0
        self.time_seconds = time_seconds

        for text in texts:
            self.remaining_texts.append(FormattedText(text, text_info))

    # DEPRECATED NEED TO FIX!!!!!
    # def update(self, typed):
    #     for text in self.running_texts:
    #         text.update(typed)
    
    # def render(self, screen):
    #     for text in self.running_texts:
    #         text.render(screen)

class RunningTextManager:
    def __init__(self, texts, text_info, avg_speed, spawn_delay):
        self.font = text_info.font
        self.remaining_texts = [] # texts that are yet to be displayed
        self.running_texts = [] # texts displayed on the screen
        #self.focused_texts = [] # texts the user is "probably" typing
        self.avg_speed = avg_speed
        self.spawn_delay = spawn_delay
        self.delay_timer = spawn_delay
        self.offscreen_valid_space = 30
        self.selected_text_id = 0
        
        # stats
        self.wpm = 0
        self.timer = 0
        self.seconds = 0
        self.total_typed = 0

        # adding texts and setting their speed and position
        for text in texts:
            new_text = FormattedText(text, text_info)
            new_text.x_speed = avg_speed * len(text) / 100
            self.remaining_texts.append(new_text)

    def change_selected_text(self, value):
        if len(self.running_texts) > 1:
            self.selected_text_id += value
            if self.selected_text_id >= len(self.running_texts):
                self.selected_text_id = 0
            elif self.selected_text_id <= -1:
                self.selected_text_id = len(self.running_texts) -1

    def update(self):
        '''Update the running texts and add new texts to the screen'''
        for r_text in self.running_texts:
            r_text.update()

        self.timer += 1
        if self.timer >= 60:
            self.timer = 0
            self.seconds += 1

        if self.delay_timer > 0:
            self.delay_timer -= 1
            if self.delay_timer <= 0:
                if len(self.remaining_texts) > 0:
                    add_text = self.remaining_texts.pop()
                    add_text.x = WIDTH
                    self.running_texts.append(add_text)
                    self.delay_timer = self.spawn_delay * 60

        # Remove texts off the screen
        for running_text in self.running_texts:
            if running_text.x + running_text.char_width * len(running_text.text) < -self.offscreen_valid_space:
                self.running_texts.remove(running_text)

        # Update the words per minute
        self.wpm = round(self.total_typed / 5) * 60 // (self.seconds + 1)
    
    def get_selected_text(self):
        if self.running_texts:
            return self.running_texts[self.selected_text_id]
        else:
            return None

    def update_total_typed(self, removed_text):
        if removed_text:
            amount = len(removed_text)
        else:
            return
        if amount:
            self.total_typed += amount
        if self.total_typed < 0:
            self.total_typed = 0

    def render(self, screen):
        # Render a rectangle around the selected text
        if len(self.running_texts):
            self.running_texts[self.selected_text_id].render_rectangle_around_selected(screen)

        # Render all texts
        for text in self.running_texts:
            text.render(screen)

        wpm_render = self.font.render('wpm: ' + str(self.wpm), True, 'white')
        screen.blit(wpm_render, (50, 50))