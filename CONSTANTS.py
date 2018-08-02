RELATIVES_CREATURE_MOVES_PER_STEP = 3 # The maximum amount of relatives (1 tile is 10 relatives) it can move on the x and y axis
DEGREES_CREATURE_ROTATES_PER_STEP = 10 # The maximum amount of degrees a creature can turn or rotate per step

MAX_LIFESPAN = 400 # The maximum amount of steps a creature can live
MAX_SENSOR_LENGTH = 30 # The maximum length in Relatives a Creatures Sensor can be

FOOD_ADDED_PER_STEP = 0.01 # The amount of food added per tile per step (The maximum food on a tile is 1)
FOOD_LOST_ON_STEP = 0.03 # The amount of food lost by a creature per step
MAX_FOOD_DIFFERNCE_FOR_NO_LOSS = 0.15 # The Difference betwwen Tile hue and mouth hue, to result in a loss of food for the creature 
MAX_FOOD_LOSS = 2 # The maximum Food Loss a Creature can suffer (Only for tile)
STARTING_SIZE = 3 # The Size of a creature with the starting food (in relatives)

MIN_WEIGHT_MUTATION = -0.05 # The minimum mutation of the neural network weights
MAX_WEIGHT_MUTATION = 0.05 # The maximum mutation of the neural network weights
N_HIDDEN_UNITS = 10

MIN_COLOR_CHANGE = -0.05 # The minimum mutation of the hue of the mouth color
MAX_COLOR_CHANGE = 0.05 # The maximum mutation of the hue of the mouth color

MIN_SENSOR_LEN_MUTATION = -5 # The minimum mutation of the sensor len
MAX_SENSOR_LEN_MUTATION = 5 # The maximum mutation of the sensor len

MIN_SENSOR_ANGLE_MUTATION = -10 # The minmum mutation of the degrees the Sensor is turned (0 is parralel to y axis)
MAX_SENSOR_ANGLE_MUTATION = 10 # The maximum mutation of the degrees the Sensor is turned (0 is parralel to y axis)

N_POPULATION = 300 # The starting population
MAX_POPULATION = 3000 # The maximum population before no more childs can be born 

MAX_CREATURE_SIZE = 10 # The maximum size of the creatures (in relatives)
FOOD_LOST_ON_NEW_CHILD = 11 # The amount a creature needs to make a new child
STARTING_FOOD = 8 # The amount of food a creature starts with
FOOD_LOST_ON_WATER = 1 # The amount a creature looses when it walks over water
EVO_STEPS_PER_FRAME = 4 # The amount of steps per frame