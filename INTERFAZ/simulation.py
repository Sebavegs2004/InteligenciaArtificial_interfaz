from importlib import reload

import numpy as np
import pygame
import random as rd
from LOGICA.DStarlite import run_DStarlite
from LOGICA.GeneticAlgorithm import GeneticAlgorithm
from button import Button
import sys
from INTERFAZ.resource_manager import ResourceManager
import os
from agent import Agente
import Color
import numpy


class Simulation:
    def __init__(self):
        self.size = None
        self.agent = None
        self.map = None
        self.size_map = None
        self.size_tile = None
        self.tile_sprites = None
        self.iteracion = 1
        self.walls = []
        self.end = None
        self.start_ticks = None
        self.running = 0
        self.prize = None
        self.prize_activated = False
        self.reset_button = Button(896, 410, 'reset')
        self.remake_button = Button(896, 500, 'remake')
        self.exit_button = Button(1080, 600, 'exit_button')
        self.agent_start_point = None
        self.surface = None
        self.simulation = None
        self.fake = None
        self.fake_pos = []

    def draw(self, surface):
        pygame.draw.rect(surface, Color.AZUL, (768, 0, 512, 720))
        # if self.iteracion != len(self.walls) - 1:
        for x in range(self.size_map):
            for y in range(self.size_map):
                surface.blit(self.tile_sprites[self.map[x][y]], (46 + y * self.size_tile, 22 + x * self.size_tile))
        if self.running == 1:
            if self.agent.move():
                self.start_ticks = pygame.time.get_ticks()
                self.running = 2
    
        if self.running == 0 and pygame.time.get_ticks() - self.start_ticks >= 3000:
            ResourceManager.music_load('death_report.mp3')
            self.running = 1
        if self.running == 2 and pygame.time.get_ticks() - self.start_ticks >= 300:
            self.iteracion = self.iteracion + 1
            self.reload_map()
            self.running = 1

        surface.blit(self.prize, (46 + (self.end[1] + 1) * self.size_tile, 22 + (self.end[0] + 1) * self.size_tile))
        if self.fake_pos != []:
            for x in self.fake_pos:
                surface.blit(self.fake,(46 + (x[0] + 1) * self.size_tile, 22 + (x[1] + 1) * self.size_tile))
        self.agent.draw(surface)

        if self.iteracion + 1 == len(self.walls) and not self.prize_activated:
            if self.agent.pos == self.end:
                ResourceManager.stop_music()
                sound = ResourceManager.sound_load('prizemortadela.mp3')
                sound.play()
                self.prize_activated = True  # marca que ya se reprodujo
            else:
                ResourceManager.stop_music()
                sound = ResourceManager.sound_load('sad.mp3')
                sound.play()
                self.prize_activated = True

        self.reset_button.draw(surface)
        self.remake_button.draw(surface)
        self.exit_button.draw(surface)
    

            

    def handle_events(self, events):
        if self.reset_button.click_event(events):
            pygame.mixer.stop()
            self.running = 0
            self.iteracion = 0
            self.start_ticks = pygame.time.get_ticks()
            sound = ResourceManager.sound_load('go123.mp3')
            sound.set_volume(0.5)
            sound.play()
            self.agent.reset()
            self.reload_map()
            self.prize_activated = False
            ResourceManager.stop_music()
        if self.remake_button.click_event(events):
            ResourceManager.stop_music()
            pygame.mixer.stop()
            if self.simulation == 'dstarlite':
                self.load_DStarlite(self.size, self.surface)
            else:
                self.load_GeneticAlgorithm(self.size, self.surface)
        if self.exit_button.click_event(events):
            ResourceManager.stop_music()
            pygame.mixer.stop()
            ResourceManager.music_load('tvtime.mp3')
            return 'selection'
        return None

    def set_borders(self):
        self.map[0][0] = 2
        self.map[0][self.size_map - 1] = 4
        self.map[self.size_map - 1][0] = 8
        self.map[self.size_map - 1][self.size_map - 1] = 6
        for x in range(self.size_map - 2):
            self.map[0][x + 1] = 3
            self.map[self.size_map - 1][x + 1] = 7
            self.map[x + 1][0] = 9
            self.map[x + 1][self.size_map - 1] = 5

        return

    def load_DStarlite(self, size, surface):
        self.fake_pos = []
        surface.blit(ResourceManager.image_load('loading.png').convert_alpha(), (400,240))
        pygame.display.flip()
        self.simulation = 'dstarlite'
        results = run_DStarlite(size)
        self.prize_activated = False
        self.surface = surface
        self.running = 0
        self.iteracion = 0
        self.end = results[1]
        self.size = size
        self.walls = results[3]
        self.map = np.zeros((size + 2, size + 2), dtype=int)
        self.size_map = len(self.map[0])
        self.size_tile = int(676 / self.size_map)
        self.set_borders()
        for x in range(size):
            for y in range(size):
                self.map[y + 1][x + 1] = self.walls[0][y][x]
        self.agent = Agente((46 + (results[0][1] + 1) * self.size_tile, 22 + (results[0][0]) * self.size_tile), 'trans', results[2], self.size_tile, results[0])
        self.agent_start_point = (self.agent.x, self.agent.y)
        self.tile_sprites = [pygame.transform.scale(ResourceManager.image_load('sand.png'), (self.size_tile, self.size_tile)).convert(), # 0
                             pygame.transform.scale(ResourceManager.image_load('wall.png'), (self.size_tile, self.size_tile)).convert(), # 1
                             pygame.transform.scale(ResourceManager.image_load('wall_corner_ul.png'), (self.size_tile, self.size_tile)).convert(),
                             pygame.transform.scale(ResourceManager.image_load('wall_up.png'), (self.size_tile, self.size_tile)).convert(),
                             pygame.transform.scale(ResourceManager.image_load('wall_corner_ur.png'), (self.size_tile, self.size_tile)).convert(),
                             pygame.transform.scale(ResourceManager.image_load('wall_right.png'), (self.size_tile, self.size_tile)).convert(),
                             pygame.transform.scale(ResourceManager.image_load('wall_corner_dr.png'), (self.size_tile, self.size_tile)).convert(),
                             pygame.transform.scale(ResourceManager.image_load('wall_down.png'), (self.size_tile, self.size_tile)).convert(),
                             pygame.transform.scale(ResourceManager.image_load('wall_corner_dl.png'), (self.size_tile, self.size_tile)).convert(),
                             pygame.transform.scale(ResourceManager.image_load('wall_left.png'), (self.size_tile, self.size_tile)).convert()]

        self.start_ticks = pygame.time.get_ticks()
        sound = ResourceManager.sound_load('go123.mp3')
        sound.set_volume(0.5)
        sound.play()
        self.prize = pygame.transform.scale(ResourceManager.image_load('premio.png'), (self.size_tile, self.size_tile))

    def load_GeneticAlgorithm(self, size, surface):
        surface.blit(ResourceManager.image_load('loading.png').convert_alpha(), (400,240))
        pygame.display.flip()
        population_size = 50
        num_generations = 50
        chromosome_length = 50
        mutation_rate = 0.01
        crossover_rate = 0.4
        genetic = GeneticAlgorithm(size, population_size, num_generations, chromosome_length, mutation_rate, crossover_rate)
        results = genetic.run()
        print(results[2])
        self.prize_activated = False
        self.surface = surface
        self.running = 0
        self.iteracion = 0
        self.simulation = 'genetic'
        self.end = results[1]
        print(len(results[3]))
        print(len(results[2]))
        self.size = size
        self.walls = results[3]
        self.map = np.zeros((size + 2, size + 2), dtype=int)
        self.size_map = len(self.map[0])
        self.size_tile = int(676 / self.size_map)
        self.set_borders()
        for x in range(size):
            for y in range(size):
                self.map[y + 1][x + 1] = self.walls[0][y][x]
        self.agent = Agente((46 + (results[0][1] + 1) * self.size_tile, 22 + (results[0][0]) * self.size_tile), 'trans', results[2], self.size_tile, results[0])
        self.agent_start_point = (self.agent.x, self.agent.y)
        self.tile_sprites = [pygame.transform.scale(ResourceManager.image_load('sand.png'), (self.size_tile, self.size_tile)).convert(), # 0
                             pygame.transform.scale(ResourceManager.image_load('wall.png'), (self.size_tile, self.size_tile)).convert(), # 1
                             pygame.transform.scale(ResourceManager.image_load('wall_corner_ul.png'), (self.size_tile, self.size_tile)).convert(),
                             pygame.transform.scale(ResourceManager.image_load('wall_up.png'), (self.size_tile, self.size_tile)).convert(),
                             pygame.transform.scale(ResourceManager.image_load('wall_corner_ur.png'), (self.size_tile, self.size_tile)).convert(),
                             pygame.transform.scale(ResourceManager.image_load('wall_right.png'), (self.size_tile, self.size_tile)).convert(),
                             pygame.transform.scale(ResourceManager.image_load('wall_corner_dr.png'), (self.size_tile, self.size_tile)).convert(),
                             pygame.transform.scale(ResourceManager.image_load('wall_down.png'), (self.size_tile, self.size_tile)).convert(),
                             pygame.transform.scale(ResourceManager.image_load('wall_corner_dl.png'), (self.size_tile, self.size_tile)).convert(),
                             pygame.transform.scale(ResourceManager.image_load('wall_left.png'), (self.size_tile, self.size_tile)).convert()]

        self.start_ticks = pygame.time.get_ticks()
        sound = ResourceManager.sound_load('go123.mp3')
        sound.set_volume(0.5)
        sound.play()
        self.prize = pygame.transform.scale(ResourceManager.image_load('premio.png'), (self.size_tile, self.size_tile))
        self.fake = pygame.transform.scale(ResourceManager.image_load('premio_fake.png'), (self.size_tile, self.size_tile))
        self.fake_pos = results[4]





    def reload_map(self):
        if self.iteracion < len(self.walls):
            for x in range(self.size):
                for y in range(self.size):
                    self.map[y + 1][x + 1] = self.walls[self.iteracion][y][x]





