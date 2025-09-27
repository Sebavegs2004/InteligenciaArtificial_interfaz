import pygame
from button import Button
import sys
from INTERFAZ.resource_manager import ResourceManager
import Color


class MainMenu:
    def __init__(self):
        self.start_button = Button(576, 380, 'genericstart')
        self.exit_button = Button(585, 480, 'genericexit')
        self.menu_title = ResourceManager.image_load('title_mortadelasimulator.png').convert_alpha()
        self.trans = ResourceManager.image_load('trans.png').convert_alpha()

    def draw(self, surface, transition = 0):
        surface.blit(self.menu_title, (329.5 , -100))
        self.start_button.draw(surface)
        self.exit_button.draw(surface)
        surface.blit(self.trans, (10, 200))

    def handle_events(self, events):
        if self.start_button.click_event(events):
            return 'selection'
        if self.exit_button.click_event(events):
            pygame.quit()
            sys.exit()
        return None

