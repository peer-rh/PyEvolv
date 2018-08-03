import numpy as np

from PyEvolv.game.CONSTANTS import *
from PyEvolv.game.Creature import Creature
from PyEvolv.game.Net import Net

class Evolution():
    def __init__(self, n_population, grid):
        """The Evolution class. It handles Giving Information to the Creatures and then converting the Creatures state and handles the proccess of Natural Selection
        
        Arguments:
            n_population {int} -- The number of starting population
            grid {np.array} -- The grid with size [len_x, len_y, 3] where each tile is [hue, saturation, value]
        """

        self.n_population = n_population
        self.grid = grid
        self.creatures_per_species_count = {}
        self.non_water_region = np.where(self.grid[:,:,2] != 0)
        self.n_species = n_population
        self._create_population()

    def next_step(self):
        """Handles Natural Selection, Feeding the Creatures brain and so on
        """

        if np.random.randint(0, 10) < 3 and NEW_SPECIES_ON_STEPS:
            self.n_species += 1
            self._new_species(self.n_species)

        for creature in self.creatures:
            if creature.dead:
                self.creatures_per_species_count[creature.species][0] -= 1
                if self.creatures_per_species_count[creature.species][0] <= 0:
                    self.creatures_per_species_count.pop(creature.species)
                self.creatures.remove(creature)
            else:
                food_added = self._calculate_food_added(creature)
                sensor_1 = self.grid[min(self.grid.shape[0]-1, int(creature.grid_sensored_tiles[0][0]/10)), min(self.grid.shape[1]-1, int(creature.grid_sensored_tiles[0][1]/10))]
                sensor_2 = self.grid[min(self.grid.shape[0]-1, int(creature.grid_sensored_tiles[1][0]/10)), min(self.grid.shape[1]-1, int(creature.grid_sensored_tiles[1][1]/10))]
                sensor_3 = self.grid[min(self.grid.shape[0]-1, int(creature.grid_sensored_tiles[2][0]/10)), min(self.grid.shape[1]-1, int(creature.grid_sensored_tiles[2][1]/10))]

                creature.next_step(food_added, sensor_1, sensor_2, sensor_3)
        for creature in self.creatures:
             if creature.get_child and len(self.creatures) < MAX_POPULATION:
                    self._create_new_child(creature)

        self.grid[self.non_water_region[0], self.non_water_region[1], 1] += FOOD_ADDED_PER_STEP
        self.grid = np.maximum(0, np.minimum(1, self.grid))


    def _create_population(self):
        """The function for randomly creating the population
        """

        self.creatures = []
        for j in range(self.n_population):
            self._new_species(j)

    def _new_species(self, species):
        weights_1 = np.random.randn(11+N_HIDDEN_UNITS, N_HIDDEN_UNITS)*0.1
        weights_2 = np.random.randn(N_HIDDEN_UNITS, N_HIDDEN_UNITS)*0.1
        weights_3 = np.random.randn(N_HIDDEN_UNITS, 4)*0.1
        net = Net(weights_1, weights_2, weights_3)
        sensors = np.concatenate([np.random.randint(0, MAX_SENSOR_LENGTH, (3)),
                                    np.random.randint(0, 360, 3)])

        i = np.random.randint(0, len(self.non_water_region[0]))
        x = self.non_water_region[0][i]*10
        y = self.non_water_region[1][i]*10
        color = (np.random.uniform(0, 1), 1, 1)
        food_color = (np.random.uniform(0, 1), 1, 1)
        size = STARTING_SIZE
        self.creatures_per_species_count[species] = [1, color]
        self.creatures.append(Creature(sensors[:2], sensors[2:4], sensors[4:6], x, y, self.grid.shape[0]*10, self.grid.shape[1]*10, color, food_color, size, net, species))
    

    def _calculate_food_added(self, creature):
        """A function for calculation the amount of food added to an creature
        
        Arguments:
            creature {Creature} -- The creature which gets fed
        
        Returns:
            float -- The amount of food which should be given to the creature
        """

        x, y = creature.relative_x, creature.relative_y
        if self.grid[int(x/10)-1,int(y/10)-1,2] == 0:
            food_given = -FOOD_LOST_ON_WATER
        else:
            food_preference = creature.food_color
            tile = self.grid[min(self.grid.shape[0]-1, int(x/10)), min(self.grid.shape[0]-1, int(y/10))]
            difference = np.abs(food_preference[0] - tile[0])
            food_given = MAX_FOOD_DIFFERNCE_FOR_NO_LOSS - difference
            food_given = max(-MAX_FOOD_LOSS, food_given) * tile[1]
            self.grid[int(x/10)-1, int(y/10)-1, 1] -= food_given
        return food_given
    
    def _create_new_child(self, creature):
        """The function for creating a child with mutation
        
        Arguments:
            creature {Creature} -- The parent creature
        """

        self.creatures_per_species_count[creature.species][0] += 1
        creature.food -= FOOD_LOST_ON_NEW_CHILD
        modification_matrix_1 = np.random.uniform(MIN_WEIGHT_MUTATION, MAX_WEIGHT_MUTATION, (11+N_HIDDEN_UNITS, N_HIDDEN_UNITS))
        modified_weights_1 = creature.net.weights_1 + modification_matrix_1
        modification_matrix_2 = np.random.uniform(MIN_WEIGHT_MUTATION, MAX_WEIGHT_MUTATION, (N_HIDDEN_UNITS, N_HIDDEN_UNITS))
        modified_weights_2 = creature.net.weights_2 + modification_matrix_2
        modification_matrix_3 = np.random.uniform(MIN_WEIGHT_MUTATION, MAX_WEIGHT_MUTATION, (N_HIDDEN_UNITS, 4))
        modified_weights_3 = creature.net.weights_3 + modification_matrix_3
        
        modified_food_color = [max(0, min(1, creature.food_color[0] + np.random.uniform(MIN_COLOR_CHANGE, MAX_COLOR_CHANGE))), 1, 1]
        modified_sensor1 = (min(MAX_SENSOR_LENGTH, creature.sensor_1[0]+np.random.randint(MIN_SENSOR_LEN_MUTATION, MAX_SENSOR_ANGLE_MUTATION)),
                            creature.sensor_1[1] + np.random.randint(MIN_SENSOR_ANGLE_MUTATION, MAX_SENSOR_ANGLE_MUTATION) % 360)
        modified_sensor2 = (min(MAX_SENSOR_LENGTH, creature.sensor_2[0]+np.random.randint(MIN_SENSOR_LEN_MUTATION, MAX_SENSOR_ANGLE_MUTATION)),
                            creature.sensor_2[1] + np.random.randint(MIN_SENSOR_ANGLE_MUTATION, MAX_SENSOR_ANGLE_MUTATION) % 360)
        modified_sensor3 = (min(MAX_SENSOR_LENGTH, creature.sensor_3[0]+np.random.randint(MIN_SENSOR_LEN_MUTATION, MAX_SENSOR_ANGLE_MUTATION)),
                            creature.sensor_3[1] + np.random.randint(MIN_SENSOR_ANGLE_MUTATION, MAX_SENSOR_ANGLE_MUTATION) % 360)
        
        net = Net(modified_weights_1, modified_weights_2, modified_weights_3)
        new_creature = Creature(modified_sensor1, modified_sensor2, modified_sensor3, 
                                creature.relative_x, creature.relative_y, 10*self.grid.shape[0], 10*self.grid.shape[1], creature.color, 
                                modified_food_color, 8, net, creature.species)
        self.creatures.append(new_creature)