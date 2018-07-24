import numpy as np
from Evo import Evolution
from game import Game
from CONSTANTS import *
import time

def main():
    grid = np.full((50, 50, 3), 222)
    evolution = Evolution(N_POPULATION, grid)
    game = Game(800, 600, grid, evolution, 100)
    while True:
        evolution.next_step()
        time.sleep(0.05)
        game.next_frame(evolution.creatures)
main()