import numpy as np
from Evo import Evolution
from game import Game
from CONSTANTS import *

def main():
    grid = np.load("grids/grid.npy")
    evolution = Evolution(N_POPULATION, grid)
    game = Game(1600, 1200, grid, evolution, 750)

    while not game.crashed:
        for _ in range(EVO_STEPS_PER_FRAME):
            evolution.next_step()
        game.update_grid(evolution.grid)
        game.next_frame(evolution.creatures, evolution.creatures_per_species_count)
main()