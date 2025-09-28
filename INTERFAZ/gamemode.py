import pygame
from button import Button
from INTERFAZ.resource_manager import ResourceManager
import Color


class GameMode:
    def __init__(self):
        self.dstar_button = Button(334, 328, 'dstar')
        self.genetic_button = Button(334 + 256 + 100, 328, 'genetico')
        self.exit_button = Button(1080, 600, 'exit_button')
        self.screamer = ResourceManager.image_load('vidal.jpg')
        self.screamer_on = 0
        self.text = ""
        self.input_active = False
        self.alpha = 255
        self.input_box = pygame.Rect(100, 80, 400, 50)
        self.font = pygame.font.Font(None, 48)
        self.color_inactive = pygame.Color('lightskyblue3')
        self.color_active = pygame.Color('dodgerblue2')
        self.color = self.color_inactive
        self.prompt_text = "Ingrese tamaño (10 <= x <= 50)"

    def draw(self, surface, transition=0):
        # Dibujar botones
        self.dstar_button.draw(surface)
        self.genetic_button.draw(surface)
        self.exit_button.draw(surface)

        # Dibujar caja blanca de fondo
        pygame.draw.rect(surface, pygame.Color('white'), self.input_box)

        # Dibujar borde
        pygame.draw.rect(surface, self.color, self.input_box, 2)

        # Renderizar texto ingresado
        txt_surface = self.font.render(self.text, True, pygame.Color('black'))
        surface.blit(txt_surface, (self.input_box.x + 5, self.input_box.y + 5))

        # Renderizar prompt al lado de la caja
        prompt_surface = self.font.render(self.prompt_text, True, Color.BLANCO)
        surface.blit(prompt_surface, (self.input_box.x + self.input_box.width + 10, self.input_box.y + 10))

    def handle_events(self, events):
        for event in events:
            # Activar/desactivar input
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.input_box.collidepoint(event.pos):
                    self.input_active = True
                else:
                    self.input_active = False
                self.color = self.color_active if self.input_active else self.color_inactive

            # Manejar teclas
            if event.type == pygame.KEYDOWN and self.input_active:
                if event.key == pygame.K_RETURN:
                    print("Texto ingresado:", self.text)
                    # Podrías validar si es número válido entre 10 y 50 aquí
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode

        # Manejar clicks de botones
        if self.dstar_button.click_event(events):
            if self.text.isdigit():  # validar input numérico
                value = int(self.text)
                if 5 <= value <= 50:
                    ret = ('simulation', value, 'dstar')
                    self.text = ""
                    return ret
                else:
                    print("El valor debe estar entre 10 y 50")
                    self.text = ""
        if self.genetic_button.click_event(events):
            if self.text.isdigit():
                value = int(self.text)
                if 5 <= value <= 50:
                    ret = ('simulation', value, 'genetic')
                    self.text = ""
                    return ret
                else:
                    print("El valor debe estar entre 10 y 50")
                    self.text = ""
        if self.exit_button.click_event(events):
            return 'main_menu'

        return None
