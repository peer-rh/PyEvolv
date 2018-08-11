from PyEvolv.main import PyEvolv
from PyEvolv.constants.constants import Constants
import argparse
import json
import numpy as np
from pathlib import Path

def main():
    kwargs = {
                "relatives_creature_moves_per_step": (int, "The maximum amount of relatives (1 tile is 10 relatives) it can move on the x and y axis"),
                "degrees_creature_rotates_per_step": (int, "The maximum amount of degrees a creature can turn or rotate per step"),
                "max_lifespan": (int, "The maximum amount of steps a creature can live"),
                "max_sensor_length": (float, "The maximum length in Relatives a Creatures Sensor can be"),
                "food_added_per_step": (float, "The amount of food added per tile per step (The maximum food on a tile is 1)"),
                "food_lost_on_step": (float, "The amount of food lost by a creature per step"),
                "max_food_differnce_for_no_loss": (float, "The Difference betwwen Tile hue and mouth hue, to result in a loss of food for the creature "),
                "max_food_loss": (float, "The maximum Food Loss a Creature can suffer (Only for tile)"),
                "starting_size": (int, "The Size of a creature with the starting food (in relatives)"),
                "min_weight_mutation": (float, "The minimum mutation of the neural network weights"),
                "max_weight_mutation": (float, "The maximum mutation of the neural network weights"),
                "n_hidden_units": (int, "The amount of hidden units in a hidden layer of the Net"),
                "min_color_change": (float, "The minimum mutation of the hue of the mouth color"),
                "max_color_change": (float, "The maximum mutation of the hue of the mouth color"),
                "min_sensor_len_mutation": (float, "The minimum mutation of the sensor len"),
                "max_sensor_len_mutation": (float, "The maximum mutation of the sensor len"),
                "min_sensor_angle_mutation": (float, "The minmum mutation of the degrees the Sensor is turned (0 is parralel to y axis)"),
                "max_sensor_angle_mutation": (float, "The maximum mutation of the degrees the Sensor is turned (0 is parralel to y axis)"),
                "n_population": (int, "The starting population"),
                "max_population": (int, "The maximum population before no more childs can be born "),
                "max_creature_size": (int, "The maximum size of the creatures (in relatives)"),
                "food_lost_on_new_child": (float, "The amount a creature needs to make a new child"),
                "starting_food": (float, "The amount of food a creature starts with"),
                "food_lost_on_water": (float, "The amount a creature looses when it walks over water"),
                "evo_steps_per_frame": (int, "The amount of steps per frame"),
                "new_species_on_steps": (bool, "If random species should be generated each step"),
                "n_creatures_per_species": (int, "The creatures spawned at the beggining with the same brain and food color and color"),
                "seed": (int, "The random seed")
            }
    parser = argparse.ArgumentParser(description='PyEvolv CLI')
    parser.add_argument('--constants_file', type=str, default="default", help="A json file with the constants")
    parser.add_argument('--height', type=int, default=650, help="The window height")
    parser.add_argument('--width', type=int, default=800, help="The window width")

    for key, definition in kwargs.items():
        parser.add_argument("--"+key, type=definition[0], default=None, help=definition[1])

    args = parser.parse_args()

    if args.constants_file == "default":
        constants = json.loads(open(str(Path.home()) + "/.pyevolv/constants.json").read())
    elif args.constants_file:
        constants = json.loads(open(args.constants_file).read())
    for i in kwargs:
        if eval("args."+i) != None:
            constants[i] = eval("args."+i)
    
    if constants["seed"] != 0:
        np.random.seed(constants["seed"])
    
    constants = Constants(constants)
    
    pe = PyEvolv(args.width, args.height, constants)
    pe.run()

if __name__=="__main__":
    main()