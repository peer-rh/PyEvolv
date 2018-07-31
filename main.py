import numpy as np
from Evo import Evolution
from game import Game
from CONSTANTS import *
import time

# TODO: Switch Tiles and food_color to HSV

def main():
    grid = np.load("grid.npy")
    evolution = Evolution(N_POPULATION, grid)
    game = Game(800, 600, grid, evolution, 750)
    while not game.crashed:
        for _ in range(EVO_STEPS_PER_FRAME):
            evolution.next_step()
        game.update_grid(evolution.grid)
        game.next_frame(evolution.creatures, evolution.creatures_per_species_count)
main()