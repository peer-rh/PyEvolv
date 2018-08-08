import numpy as np
from PyEvolv.evolution.Creature import Creature
from PyEvolv.evolution.Net import Net
from typing import Dict, Tuple, List, Union

class Evolution():
    def __init__(self, n_population: int, grid: np.ndarray, constants: Dict) -> None:
        """The Evolution class. It handles Giving Information to the Creatures and then converting the Creatures state and handles the proccess of Natural Selection
        
        Arguments:
            n_population {int} -- The number of starting population
            grid {np.array} -- The grid with size [len_x, len_y, 3] where each tile is [hue, saturation, value]
        """

        self.n_population = n_population
        self.grid = grid
        self.constants = constants
        self.creatures_per_species_count: Dict[Union[int, List[int, Tuple[float, float, float]]]] = {}
        self.non_water_region = np.where(self.grid[:,:,2] != 0)
        self.n_species = n_population
        self._create_population()

    def next_step(self) -> None:
        """Handles Natural Selection, Feeding the Creatures brain and so on
        """

        if np.random.randint(0, 10) < 3 and self.constants["new_species_on_steps"]:
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
             if creature.get_child and len(self.creatures) < self.constants["max_population"]:
                    self._create_new_child(creature)

        self.grid[self.non_water_region[0], self.non_water_region[1], 1] += self.constants["food_added_per_step"]
        self.grid = np.maximum(0, np.minimum(1, self.grid))


    def _create_population(self) -> None:
        """The function for randomly creating the population
        """

        self.creatures: List[Creature] = []
        for j in range(self.n_population//self.constants["n_creatures_per_species"]):
            weights_1 = np.random.randn(11+self.constants["n_hidden_units"], self.constants["n_hidden_units"])*0.1
            weights_2 = np.random.randn(self.constants["n_hidden_units"], self.constants["n_hidden_units"])*0.1
            weights_3 = np.random.randn(self.constants["n_hidden_units"], 4)*0.1
            net = Net(weights_1, weights_2, weights_3)
            sensors = np.concatenate([np.random.randint(0, self.constants["max_sensor_length"], 3),
                                        np.random.randint(0, 360, 3)])

            sensor_1: Tuple[int, int] = tuple(sensors[:2])
            sensor_2: Tuple[int, int] = tuple(sensors[2:4])
            sensor_3: Tuple[int, int] = tuple(sensors[4:6])
            color = (np.random.uniform(0, 1), 1, 1)
            food_color = (np.random.uniform(0, 1), 1, 1)
            for _ in range(self.constants["n_creatures_per_species"]):
                i = np.random.randint(0, len(self.non_water_region[0]))
                x = self.non_water_region[0][i]*10
                y = self.non_water_region[1][i]*10
                size = self.constants["starting_size"]
                self.creatures_per_species_count[j] = [self.constants["n_creatures_per_species"], color]
                self.creatures.append(Creature(sensor_1, sensor_2, sensor_3, x, y, self.grid.shape[0]*10, self.grid.shape[1]*10, color, food_color, size, net, j, self.constants))

    def _new_species(self, species:int) -> None:
        weights_1 = np.random.randn(11+self.constants["n_hidden_units"], self.constants["n_hidden_units"])*0.1
        weights_2 = np.random.randn(self.constants["n_hidden_units"], self.constants["n_hidden_units"])*0.1
        weights_3 = np.random.randn(self.constants["n_hidden_units"], 4)*0.1
        net = Net(weights_1, weights_2, weights_3)
        sensors = np.concatenate([np.random.randint(0, self.constants["max_sensor_length"], (3)),
                                    np.random.randint(0, 360, 3)])

        sensor_1: Tuple[int, int] = tuple(sensors[:2])
        sensor_2: Tuple[int, int] = tuple(sensors[2:4])
        sensor_3: Tuple[int, int] = tuple(sensors[4:6])

        i = np.random.randint(0, len(self.non_water_region[0]))
        x = self.non_water_region[0][i]*10
        y = self.non_water_region[1][i]*10
        color = (np.random.uniform(0, 1), 1, 1)
        food_color = (np.random.uniform(0, 1), 1, 1)
        size = self.constants["starting_size"]
        self.creatures_per_species_count[species] = [1, color]
        self.creatures.append(Creature(sensor_1, sensor_2, sensor_3, x, y, self.grid.shape[0]*10, self.grid.shape[1]*10, color, food_color, size, net, species, self.constants))
    

    def _calculate_food_added(self, creature: Creature) -> float:
        """A function for calculation the amount of food added to an creature
        
        Arguments:
            creature {Creature} -- The creature which gets fed
        
        Returns:
            float -- The amount of food which should be given to the creature
        """

        x, y = creature.relative_x, creature.relative_y
        if self.grid[int(x/10)-1,int(y/10)-1,2] == 0:
            food_given = -self.constants["food_lost_on_water"]
        else:
            food_preference = creature.food_color
            tile = self.grid[min(self.grid.shape[0]-1, int(x/10)), min(self.grid.shape[0]-1, int(y/10))]
            difference = np.abs(food_preference[0] - tile[0])
            food_given = self.constants["max_food_differnce_for_no_loss"] - difference
            food_given = max(-self.constants["max_food_loss"], food_given) * tile[1]
            self.grid[int(x/10)-1, int(y/10)-1, 1] -= food_given
        return food_given
    
    def _create_new_child(self, creature: Creature) -> None:
        """The function for creating a child with mutation
        
        Arguments:
            creature {Creature} -- The parent creature
        """

        self.creatures_per_species_count[creature.species][0] += 1
        creature.food -= self.constants["food_lost_on_new_child"]
        modification_matrix_1 = np.random.uniform(self.constants["min_weight_mutation"], self.constants["max_weight_mutation"], (11+self.constants["n_hidden_units"], self.constants["n_hidden_units"]))
        modified_weights_1 = creature.net.weights_1 + modification_matrix_1
        modification_matrix_2 = np.random.uniform(self.constants["min_weight_mutation"], self.constants["max_weight_mutation"], (self.constants["n_hidden_units"], self.constants["n_hidden_units"]))
        modified_weights_2 = creature.net.weights_2 + modification_matrix_2
        modification_matrix_3 = np.random.uniform(self.constants["min_weight_mutation"], self.constants["max_weight_mutation"], (self.constants["n_hidden_units"], 4))
        modified_weights_3 = creature.net.weights_3 + modification_matrix_3
        
        modified_food_color = (max(0, min(1, creature.food_color[0] + np.random.uniform(self.constants["min_color_change"], self.constants["max_color_change"]))), 1, 1)
        modified_sensor1 = (min(self.constants["max_sensor_length"], creature.sensor_1[0]+np.random.randint(self.constants["min_sensor_len_mutation"], self.constants["max_sensor_angle_mutation"])),
                            creature.sensor_1[1] + np.random.randint(self.constants["min_sensor_angle_mutation"], self.constants["max_sensor_angle_mutation"]) % 360)
        modified_sensor2 = (min(self.constants["max_sensor_length"], creature.sensor_2[0]+np.random.randint(self.constants["min_sensor_len_mutation"], self.constants["max_sensor_angle_mutation"])),
                            creature.sensor_2[1] + np.random.randint(self.constants["min_sensor_angle_mutation"], self.constants["max_sensor_angle_mutation"]) % 360)
        modified_sensor3 = (min(self.constants["max_sensor_length"], creature.sensor_3[0]+np.random.randint(self.constants["min_sensor_len_mutation"], self.constants["max_sensor_angle_mutation"])),
                            creature.sensor_3[1] + np.random.randint(self.constants["min_sensor_angle_mutation"], self.constants["max_sensor_angle_mutation"]) % 360)
        
        net = Net(modified_weights_1, modified_weights_2, modified_weights_3)
        new_creature = Creature(modified_sensor1, modified_sensor2, modified_sensor3, 
                                creature.relative_x, creature.relative_y, 10*self.grid.shape[0], 10*self.grid.shape[1], creature.color, 
                                modified_food_color, 8, net, creature.species, self.constants)
        self.creatures.append(new_creature)