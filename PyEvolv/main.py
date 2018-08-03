import numpy as np
from PyEvolv.game.Evo import Evolution
from PyEvolv.game.game import Game
from PyEvolv.grid_creator.grid_creator import GridCreator
from PyEvolv.start_screen import StartingScreen
from PyEvolv.game.CONSTANTS import *
from PyEvolv.assets.font import FONT
import pygame
import os

class PyEvolv:
    def __init__(self, width, height, bg_color=(255,255,255), primary_color=(0,0,0), secondary_color=(0,0,255)):
        self.width = width
        self.height = height
        self.bg_color = bg_color
        self.primary_color = primary_color
        self.secondary_color = secondary_color

        self.grids_path = "/".join(os.path.realpath(__file__).split("/")[:-2])+"/grids"

        pygame.init()
        self.gameDisplay = pygame.display.set_mode((self.width, self.height))
        self.current_env = "start_screen"

        self.starting_screen = StartingScreen(self.height, self.width, self.bg_color, self.primary_color, self.secondary_color)

        self.back_txt = FONT.render("<BACK", False, self.primary_color)

        self.game = None
        self.evolution = None
        self.grid_creator = None

    def run(self):
        crashed = False
        while not crashed:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    crashed = True

                self._controller(event)

                if self.current_env == "start_screen":
                    self.starting_screen.starting_screen_controller(event)
                if self.current_env == "game":
                    try:
                        self.game.controller(event)
                    except:
                        pass
                if self.current_env == "grid_creator":
                    try:
                        self.grid_creator.controller(event)
                    except:
                        pass

            self._next_frame()
            pygame.display.update()


    def _next_frame(self):
        if self.current_env == "start_screen":
            self._starting_screen_bridge()
            self.starting_screen.next_frame()
            self.gameDisplay.blit(self.starting_screen.surf, (0,0))
        
        elif self.current_env == "game":
            self.gameDisplay.fill((255, 0, 0))
            pygame.draw.rect(self.gameDisplay, self.bg_color, (0,0,self.width, 50))
            self.gameDisplay.blit(self.back_txt, (15, 15))

            if self.game == None:
                self._generate_game()
            for _ in range(EVO_STEPS_PER_FRAME):
                self.evolution.next_step()
            
            self.game.update_grid(self.evolution.grid)
            self.game.next_frame(self.evolution.creatures, self.evolution.creatures_per_species_count)
            self.gameDisplay.blit(self.game.surf, (0, 50))

        elif self.current_env == "grid_creator":
            self.gameDisplay.fill((0, 255, 0))
            pygame.draw.rect(self.gameDisplay, self.bg_color, (0,0,self.width, 50))
            self.gameDisplay.blit(self.back_txt, (15, 15))
            if self.grid_creator == None:
                self._generate_grid_creator()
            self.grid_creator.next_frame()
            self.gameDisplay.blit(self.grid_creator.surf, (0, 50))
            
    def _controller(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.current_env != "start_screen" and 0 < event.pos[0] < self.back_txt.get_rect().width + 15 and 0 < event.pos[1] < 50:
                self.current_env = "start_screen"
                self.grid_creator = None
                self.game = None
                self.evolution = None
    
    def _starting_screen_bridge(self):
        if self.starting_screen.game:
            self.current_env = "game"
            self.starting_screen.game = False
        
        elif self.starting_screen.grid_creator:
            self.current_env = "grid_creator"
            self.starting_screen.grid_creator = False
    
    def _generate_game(self):
        grid = np.load(self.grids_path + "/grid.npy")
        self.evolution = Evolution(N_POPULATION, grid)
        self.game = Game(self.width, self.height-50, grid, 
                        self.evolution, 750)
    
    def _generate_grid_creator(self):
        self.grid_creator = GridCreator(self.width, self.height-50, np.zeros((75, 75, 3)), self.grids_path+"/", 750, 50, self.bg_color, self.primary_color, self.secondary_color)