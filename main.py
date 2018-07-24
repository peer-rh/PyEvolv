import numpy as np
from Evo import Evolution
from game import Game
from CONSTANTS import *
import time

# TODO: Switch Tiles and food_color to HSV

def main():
    grid = np.random.randint(200, 255, (50, 50, 3))
    evolution = Evolution(N_POPULATION, grid)
    game = Game(800, 600, grid, evolution, 100)
    while True:
        evolution.next_step()
        time.sleep(0.05)
        game.update_grid(evolution.grid)
        game.next_frame(evolution.creatures)
main()