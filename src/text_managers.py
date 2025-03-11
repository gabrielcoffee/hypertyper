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

    def update(self, typed):
        for text in self.running_texts:
            text.update(typed)
    
    def render(self, screen):
        for text in self.running_texts:
            text.render(screen)

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
                
    def update_typing(self, typed):
        self.running_texts[self.selected_text_id].update_typing(typed)

        self.wpm = round(self.total_typed / 5) * 60 // (self.seconds + 1)
    
    def render(self, screen):
        # render on the selected text a rectangle around it
        if len(self.running_texts):
            self.running_texts[self.selected_text_id].render_rectangle_around_selected(screen)


        for text in self.running_texts:
            text.render(screen)

        wpm_render = self.font.render('wpm: ' + str(self.wpm), True, 'white')
        screen.blit(wpm_render, (50, 50))