import numpy as np
from PyEvolv.game.Evo import Evolution
from PyEvolv.game.game import Game
from PyEvolv.start_screen import StartingScreen
from PyEvolv.game.CONSTANTS import *
import pygame
import os

# TODO: Switch Tiles and food_color to HSV

def main():
    grid = np.load("/".join(os.path.realpath(__file__).split("/")[:-2])+"/grids/grid.npy")
    evolution = Evolution(N_POPULATION, grid)
    game = Game(1600, 1200, grid, evolution, 750)
    while not game.crashed:
        for _ in range(EVO_STEPS_PER_FRAME):
            evolution.next_step()
        game.update_grid(evolution.grid)
        game.next_frame(evolution.creatures, evolution.creatures_per_species_count)
if __name__ == "__main__":
    main()

class PyEvolv:
    def __init__(self, width, height, bg_color=(255,255,255), primary_color=(0,0,0), secondary_color=(0,0,255)):
        self.width = width
        self.height = height
        self.bg_color = bg_color
        self.primary_color = primary_color
        self.secondary_color = secondary_color

        pygame.init()
        self.gameDisplay = pygame.display.set_mode((self.width, self.height))
        self.current_env = "start_screen"

        self.starting_screen = StartingScreen(self.height, self.width, self.bg_color, self.primary_color, self.secondary_color)
    
    def run(self):
        crashed = False
        while not crashed:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    crashed = True

                if self.current_env == "start_screen":
                    self.starting_screen.starting_screen_controller(event)

            self._next_frame()
            pygame.display.update()
    
    def _next_frame(self):
        if self.current_env == "start_screen":
            self._starting_screen_bridge()
            self.starting_screen.next_frame()
            self.gameDisplay.blit(self.starting_screen.surf, (0,0))
        
        elif self.current_env == "game":
            self.gameDisplay.fill((255, 0, 0))
            pygame.draw.rect()

        elif self.current_env == "grid_creator":
            self.gameDisplay.fill((0, 255, 0))
            pygame.draw.rect()
        

    
    def _starting_screen_bridge(self):
        if self.starting_screen.game:
            self.current_env = "game"
            self.starting_screen.game = False
        
        elif self.starting_screen.grid_creator:
            self.current_env = "grid_creator"
            self.starting_screen.grid_creator = False