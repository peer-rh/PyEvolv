import numpy as np
from PyEvolv.evolution.Evo import Evolution
from PyEvolv.game.game import Game
from PyEvolv.grid_creator.grid_creator import GridCreator
from PyEvolv.screens.start_screen import StartingScreen
from PyEvolv.assets.font import FONT
import pygame
from pathlib import Path
import os
from typing import Dict, List, Tuple

class PyEvolv:
    def __init__(self, width:int, height:int, constants, bg_color:Tuple[int, int, int]=(255,255,255), primary_color:Tuple[int, int, int]=(0,0,0), secondary_color:Tuple[int, int, int]=(0,0,255)) -> None:
        self.width = width
        self.height = height
        self.constants = constants
        self.bg_color = bg_color
        self.primary_color = primary_color
        self.secondary_color = secondary_color

        self.grids_path = str(Path.home()) + "/.pyevolv/grids/"

        pygame.init()
        self.gameDisplay = pygame.display.set_mode((self.width, self.height))
        self.current_env = "start_screen"

        self.starting_screen = StartingScreen(self.height, self.width, self.bg_color, self.primary_color, self.secondary_color)

        self.back_txt = FONT.render("<BACK", False, self.primary_color)

        self.game: Game = None
        self.evolution: Evolution = None
        self.grid_creator: GridCreator = None

    def run(self) -> None:
        crashed = False
        while not crashed:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    crashed = True

                self._controller(event)

                if self.current_env == "start_screen":
                    self.starting_screen.starting_screen_controller(event)
                elif self.current_env == "game":
                    try:
                        self.game.controller(event, self.evolution.creature_locations)
                    except Exception as e:
                        raise e
                elif self.current_env == "grid_creator":
                    try:
                        self.grid_creator.controller(event)
                    except Exception as e:
                        raise e
                
            
            self._next_frame()
            pygame.display.update()


    def _next_frame(self) -> None:
        if self.current_env == "start_screen":
            self._starting_screen_bridge()
            self.starting_screen.next_frame()
            self.gameDisplay.blit(self.starting_screen.surf, (0,0))
        
        elif self.current_env == "game":
            pygame.draw.rect(self.gameDisplay, self.bg_color, (0,0,self.width, 50))
            self.gameDisplay.blit(self.back_txt, (15, 15))

            if self.game == None:
                self._generate_game()
            for _ in range(self.constants["evo_steps_per_frame"]):
                self.evolution.next_step()
            
            self.game.update_grid(self.evolution.grid)
            self.game.next_frame(self.evolution.herbivores, self.evolution.carnivores, self.evolution.creatures_per_species_count, self.evolution.creature_locations)
            self.gameDisplay.blit(self.game.surf, (0, 50))

        elif self.current_env == "grid_creator":
            pygame.draw.rect(self.gameDisplay, self.bg_color, (0,0,self.width, 50))
            self.gameDisplay.blit(self.back_txt, (15, 15))
            if self.grid_creator == None:
                self._generate_grid_creator()
            self.grid_creator.next_frame()
            self.gameDisplay.blit(self.grid_creator.surf, (0, 50))
        
        
            
    def _controller(self, event:pygame.event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.current_env != "start_screen" and 0 < event.pos[0] < self.back_txt.get_rect().width + 15 and 0 < event.pos[1] < 50:
                self.current_env = "start_screen"
                self.starting_screen._generate_background()
                self.grid_creator = None
                self.game = None
                self.evolution = None

    
    def _starting_screen_bridge(self) -> None:
        if self.starting_screen.game:
            self.current_env = "game"
            self.starting_screen.game = False
        
        elif self.starting_screen.grid_creator:
            self.current_env = "grid_creator"
            self.starting_screen.grid_creator = False
        
    
    def _generate_game(self) -> None:
        grid = np.load(self.grids_path + "/grid.npy")
        self.evolution = Evolution(grid, self.constants)
        self.game = Game(self.width, self.height-50, 50, grid, 750, self.constants)
    
    def _generate_grid_creator(self) -> None:
        self.grid_creator = GridCreator(self.width, self.height-50, np.zeros((75, 75, 3)), self.grids_path+"/", 750, 50, self.bg_color, self.primary_color, self.secondary_color)
    
    