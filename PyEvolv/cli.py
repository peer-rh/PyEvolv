from PyEvolv.main import PyEvolv
import argparse
import json
from pathlib import Path

def main():

    parser = argparse.ArgumentParser(description='PyEvolv CLI')
    parser.add_argument('--constants_file', type=str, default=None, help="A json file with the constants")
    parser.add_argument("--relatives_creature_moves_per_step", type=int, default=6, help="The maximum amount of relatives (1 tile is 10 relatives) it can move on the x and y axis")
    parser.add_argument("--degrees_creature_rotates_per_step", type=int, default=10, help="The maximum amount of degrees a creature can turn or rotate per step")
    parser.add_argument("--max_lifespan", type=int, default=400, help="The maximum amount of steps a creature can live")
    parser.add_argument("--max_sensor_length", type=float,default=30, help="The maximum length in Relatives a Creatures Sensor can be")
    parser.add_argument("--food_added_per_step", type=float,default=0.01, help="The amount of food added per tile per step (The maximum food on a tile is 1)")
    parser.add_argument("--food_lost_on_step", type=float,default=0.05, help="The amount of food lost by a creature per step")
    parser.add_argument("--max_food_differnce_for_no_loss", type=float,default=0.13, help="The Difference betwwen Tile hue and mouth hue, to result in a loss of food for the creature ")
    parser.add_argument("--max_food_loss", type=float,default=2, help="The maximum Food Loss a Creature can suffer (Only for tile)")
    parser.add_argument("--starting_size", type=int, default=3, help="The Size of a creature with the starting food (in relatives)")
    parser.add_argument("--min_weight_mutation", type=float,default=-0.005, help="The minimum mutation of the neural network weights")
    parser.add_argument("--max_weight_mutation", type=float,default=0.005, help="The maximum mutation of the neural network weights")
    parser.add_argument("--n_hidden_units", type=int, default=30, help="The amount of hidden units in a hidden layer of the Net")
    parser.add_argument("--min_color_change", type=float,default=-0.05, help="The minimum mutation of the hue of the mouth color")
    parser.add_argument("--max_color_change", type=float,default=0.05, help="The maximum mutation of the hue of the mouth color")
    parser.add_argument("--min_sensor_len_mutation", type=float,default=-5, help="The minimum mutation of the sensor len")
    parser.add_argument("--max_sensor_len_mutation", type=float,default=5, help="The maximum mutation of the sensor len")
    parser.add_argument("--min_sensor_angle_mutation", type=float,default=-10, help="The minmum mutation of the degrees the Sensor is turned (0 is parralel to y axis)")
    parser.add_argument("--max_sensor_angle_mutation", type=float,default=10, help="The maximum mutation of the degrees the Sensor is turned (0 is parralel to y axis)")
    parser.add_argument("--n_population", type=int, default=300, help="The starting population")
    parser.add_argument("--max_population", type=int, default=3000, help="The maximum population before no more childs can be born ")
    parser.add_argument("--max_creature_size", type=int, default=10, help="The maximum size of the creatures (in relatives)")
    parser.add_argument("--food_lost_on_new_child", type=float,default=14, help="The amount a creature needs to make a new child")
    parser.add_argument("--starting_food", type=float,default=8, help="The amount of food a creature starts with")
    parser.add_argument("--food_lost_on_water", type=float,default=3, help="The amount a creature looses when it walks over water")
    parser.add_argument("--evo_steps_per_frame", type=int, default=3, help="The amount of steps per frame")
    parser.add_argument("--new_species_on_steps", type=bool, default=True, help="If random species should be generated each step")
    parser.add_argument("--n_creatures_per_species", type=int, default=2, help="The creatures spawned at the beggining with the same brain and food color and color")
    args = parser.parse_args()

    if args.constants_file == "default":
        constants = json.loads(open(str(Path.home()) + "/.pyevolv/constants.json").read())
    elif args.constants_file:
        constants = json.loads(open(args.constants_file).read())
    else:
        constants = {
            "relatives_creature_moves_per_step": args.relatives_creature_moves_per_step,
            "degrees_creature_rotates_per_step": args.degrees_creature_rotates_per_step,
            "max_lifespan": args.max_lifespan,
            "max_sensor_length": args.max_sensor_length,
            "food_added_per_step": args.food_added_per_step,
            "food_lost_on_step": args.food_lost_on_step,
            "max_food_differnce_for_no_loss": args.max_food_differnce_for_no_loss,
            "max_food_loss": args.max_food_loss,
            "starting_size": args.starting_size,
            "min_weight_mutation": args.min_weight_mutation,
            "max_weight_mutation": args.max_weight_mutation,
            "n_hidden_units": args.n_hidden_units,
            "min_color_change": args.min_color_change,
            "max_color_change": args.max_color_change,
            "min_sensor_len_mutation": args.min_sensor_len_mutation,
            "max_sensor_len_mutation": args.max_sensor_len_mutation,
            "min_sensor_angle_mutation": args.min_sensor_angle_mutation,
            "max_sensor_angle_mutation": args.max_sensor_angle_mutation,
            "n_population": args.n_population,
            "max_population": args.max_population,
            "max_creature_size": args.max_creature_size,
            "food_lost_on_new_child": args.food_lost_on_new_child,
            "starting_food": args.starting_food,
            "food_lost_on_water": args.food_lost_on_water,
            "evo_steps_per_frame": args.evo_steps_per_frame,
            "new_species_on_steps": args.new_species_on_steps,
            "n_creatures_per_species": args.n_creatures_per_species
        }
    
    pe = PyEvolv(800, 650, constants)
    pe.run()