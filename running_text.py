import random
from globals import WIDTH, HEIGHT

class RunningText:
    '''Represents a running text on the screen'''
    def __init__(self, text, speed, font):
        self.text_render = font.render(text, True, (255,255,255))
        self.text = text
        self.speed = speed
        self.font = font
        self.x = 800
        self.y = random.randint(200, 400)

    def update(self):
        self.x -= self.speed

    def render(self, screen):
        screen.blit(self.text_render, (self.x, self.y))

class RunningTextManager:
    '''Manages the running texts that are displayed on the screen'''
    def __init__(self, texts, max_texts_running, max_text_speed, font):
        # Parameter initialization
        self.remaining_texts = texts
        self.max_texts_running = max_texts_running
        self.max_text_speed = max_text_speed
        self.font = font

        # Default class variables
        self.start_delay = 60 * 3
        self.delay_timer = 0
        self.running_texts = []
    
    def add_text_to_list(self, text):
        '''Add a text to list of remaining texts that will later be displayed'''
        self.remaining_texts.append(text)

    def remove_text_match(self, input_text) -> bool:
        '''Remove a text from the running texts if it matches the input by the player

        :return: Return True if found a match and removed of False otherwise
        '''
        for i in range(len(self.running_texts)):
            if self.running_texts[i].text == input_text:
                self.running_texts.pop(i)
                return True
        return False

    def update(self):
        '''Update the running texts and add new texts if there are less than the maximum texts running'''
        for text in self.running_texts:
            text.update()

        if self.delay_timer > 0:
            self.delay_timer -= 1

        # Add new text to running texts if there are less than maximum texts running
        if len(self.running_texts) < self.max_texts_running and self.delay_timer <= 0:
            if self.remaining_texts:
                random_text_index = random.randint(0, len(self.remaining_texts)-1)
                random_speed = random.randint(1, self.max_text_speed)

                running_text = RunningText(self.remaining_texts.pop(random_text_index), random_speed, self.font)
                self.running_texts.append(running_text)
                self.delay_timer = self.start_delay

        # Remove texts off the screen
        for running_text in self.running_texts:
            if running_text.x + running_text.text_render.get_width() < 0:
                self.running_texts.remove(running_text)
    
    def render(self, screen):
        '''Render the running texts on the screen'''
        for running_text in self.running_texts:
            running_text.render(screen)
    