import numpy as np
from PyEvolv.creatures.Herbivore import Herbivore
from PyEvolv.creatures.Carnivore import Carnivore
from PyEvolv.creatures.Creature import Creature
from PyEvolv.evolution.Net import Net
from typing import Dict, Tuple, List, Union

class Evolution():
    def __init__(self, grid: np.ndarray, constants: Dict) -> None:
        """The Evolution class. It handles Giving Information to the Creatures and then converting the Creatures state and handles the proccess of Natural Selection
        
        Arguments:
            n_population {int} -- The number of starting population
            grid {np.array} -- The grid with size [len_x, len_y, 3] where each tile is [hue, saturation, value]
        """

        self.n_herbivores: int = constants["n_herbivores"]
        self.n_carnivores: int = constants["n_carnivores"]
        self.herbivore_chance: float = self.n_herbivores / (self.n_herbivores+self.n_carnivores)
        self.grid = grid
        self.constants = constants
        self.creatures_per_species_count: Dict[Union[int, List[int, Tuple[float, float, float]]]] = {}
        self.non_water_region: np.ndarray = np.where(self.grid[:,:,2] != 0)
        self.n_species = self.n_herbivores // self.constants["n_creatures_per_species"] + self.n_carnivores // self.constants["n_creatures_per_species"]
        self.creature_locations: Dict[Creature, Tuple[int, int]] = {}
        self._create_population()

    def next_step(self) -> None:
        """Handles Natural Selection, Feeding the Creatures brain and so on
        """

        if np.random.randint(0, 10) < 3 and self.constants["new_species_on_steps"]:
            self.n_species += 1
            if np.random.uniform() < self.herbivore_chance:
                self._new_species("Herbivore", self.n_species)
            else:
                self._new_species("Carnivore", self.n_species)


        for herbivore in self.herbivores:
            if herbivore.dead:
                self.creatures_per_species_count[herbivore.species][0] -= 1
                if self.creatures_per_species_count[herbivore.species][0] <= 0:
                    self.creatures_per_species_count.pop(herbivore.species)
                self.herbivores.remove(herbivore)
                del self.creature_locations[herbivore]
            else:
                food_added = self._calculate_food_added_herbivore(herbivore)

                sensor_1 = self.grid[min(self.grid.shape[0]-1, int(herbivore.grid_sensored_tiles[0][0]/10)), min(self.grid.shape[1]-1, int(herbivore.grid_sensored_tiles[0][1]/10))]
                sensor_2 = self.grid[min(self.grid.shape[0]-1, int(herbivore.grid_sensored_tiles[1][0]/10)), min(self.grid.shape[1]-1, int(herbivore.grid_sensored_tiles[1][1]/10))]
                sensor_3 = self.grid[min(self.grid.shape[0]-1, int(herbivore.grid_sensored_tiles[2][0]/10)), min(self.grid.shape[1]-1, int(herbivore.grid_sensored_tiles[2][1]/10))]

                herbivore.next_step(food_added, sensor_1, sensor_2, sensor_3)
                self.creature_locations[herbivore] = (int(herbivore.relative_x), int(herbivore.relative_y))

        for herbivore in self.herbivores:
            if herbivore.get_child and len(self.herbivores) + len(self.carnivores) < self.constants["max_population"]:
                self._create_new_child(herbivore)

        for carnivore in self.carnivores:
            if carnivore.dead:
                self.creatures_per_species_count[carnivore.species][0] -= 1
                if self.creatures_per_species_count[carnivore.species][0] <= 0:
                    self.creatures_per_species_count.pop(carnivore.species)
                self.carnivores.remove(carnivore)
                del self.creature_locations[carnivore]
            else:
                food_added = self._calculate_food_added_carnivore(carnivore)

                sensor_1, sensor_2, sensor_3 = self._get_sensor_data_carnivore(carnivore.grid_sensored_tiles)
                
                carnivore.next_step(food_added, sensor_1, sensor_2, sensor_3)
                self.creature_locations[carnivore] = (int(carnivore.relative_x), int(carnivore.relative_y))

        for carnivore in self.carnivores:
            if carnivore.get_child and len(self.herbivores) + len(self.carnivores) < self.constants["max_population"]:
                self._create_new_child(carnivore)
        
        self.grid[self.non_water_region[0], self.non_water_region[1], 1] += self.constants["food_added_per_step"]
        self.grid = np.maximum(0, np.minimum(1, self.grid))


    def _create_population(self) -> None:
        """The function for randomly creating the population
        """
        self.herbivores: List[Herbivore] = []
        self.carnivores: List[Carnivore] = []
        
        for j in range(self.n_herbivores//self.constants["n_creatures_per_species"]):
            self._new_species("Herbivore", j)
        for j in range(self.n_carnivores//self.constants["n_creatures_per_species"]):
            self._new_species("Carnivore", j + self.n_herbivores//self.constants["n_creatures_per_species"])
    
    def _new_species(self, type:str, species:int) -> None:
        weights_1 = np.random.randn(11+self.constants["n_hidden_units"], self.constants["n_hidden_units"])*0.1
        weights_2 = np.random.randn(self.constants["n_hidden_units"], self.constants["n_hidden_units"])*0.1
        weights_3 = np.random.randn(self.constants["n_hidden_units"], 4)*0.1
        net = Net(weights_1, weights_2, weights_3)
        sensors = np.concatenate([np.random.randint(0, self.constants["max_sensor_length"], (3)),
                                    np.random.randint(0, 360, 3)])

        sensor_1: Tuple[int, int] = tuple(sensors[:2])
        sensor_2: Tuple[int, int] = tuple(sensors[2:4])
        sensor_3: Tuple[int, int] = tuple(sensors[4:6])

        for _ in range(self.constants["n_creatures_per_species"]):
            i = np.random.randint(0, len(self.non_water_region[0]))
            x = self.non_water_region[0][i]*10
            y = self.non_water_region[1][i]*10
            color = (np.random.uniform(0, 1), 1, 1)
            food_color = (np.random.uniform(0, 1), 1, 1)
            size = self.constants["starting_size"]
            self.creatures_per_species_count[species] = [self.constants["n_creatures_per_species"], color]
            if type == "Herbivore":
                creature: Union[Herbivore, Creature] = Herbivore(sensor_1, sensor_2, sensor_3, x, y, self.grid.shape[0]*10, self.grid.shape[1]*10, color, food_color, size, net, species, self.constants)
                self.herbivores.append(creature)
            elif type == "Carnivore":
                creature: Union[Herbivore, Creature] = Carnivore(sensor_1, sensor_2, sensor_3, x, y, self.grid.shape[0]*10, self.grid.shape[1]*10, color, food_color, size, net, species, self.constants)
                self.carnivores.append(creature)

            self.creature_locations[creature] = (x, y)    

    def _calculate_food_added_herbivore(self, creature: Herbivore) -> float:
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
   
    def _calculate_food_added_carnivore(self, carnivore: Carnivore) -> float: # TODO: Add optimization
        """A function for calculation the amount of food added to an creature
        
        Arguments:
            creature {Creature} -- The creature which gets fed
        
        Returns:
            float -- The amount of food which should be given to the creature
        """

        x, y = carnivore.relative_x, carnivore.relative_y
        locs = np.asarray(list(self.creature_locations.values()))
        if self.constants["carnivore_eat_range"] == "size":
            eat_range: int = carnivore.size
        else:
            eat_range = self.constants["carnivore_eat_range"]
        creatures_to_eat_from: np.ndarray = np.asarray(list(self.creature_locations.keys()))[np.where((locs[:, 0] < x + eat_range)
                                                                                            & (x - eat_range < locs[:, 0])
                                                                                            & (locs[:, 1] < y + eat_range)
                                                                                            & (y - eat_range < locs[:, 1]))] # checks which creatures are in his eating range
        
        if len(creatures_to_eat_from) != 0:
            creature_info: List[Tuple[Tuple[float, float, float], float]] = [(creature.color, creature.food) for creature in creatures_to_eat_from]
            creature_returns: List[float] = [max(-self.constants["max_food_loss"], self.constants["max_food_differnce_for_no_loss"] - np.abs(carnivore.food_color[0] - creature[0][0]))*min(1,creature[1]) for creature in creature_info]
            best_creature_index = np.argmax(creature_returns)
            best_creature_return = creature_returns[best_creature_index]
            print(best_creature_return)
            creatures_to_eat_from[best_creature_index].food = max(0, -best_creature_return) # so that creature wont get more food by loss of creature
        else:
            best_creature_return = 0

        return best_creature_return
    
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
        if creature.type == "Herbivore":
            new_creature: Union[Herbivore, Creature] = Herbivore(modified_sensor1, modified_sensor2, modified_sensor3, 
                                creature.relative_x, creature.relative_y, 10*self.grid.shape[0], 10*self.grid.shape[1], creature.color, 
                                modified_food_color, 8, net, creature.species, self.constants)
            self.herbivores.append(new_creature)

        elif creature.type == "Carnivore":
            new_creature: Union[Herbivore, Creature] = Carnivore(modified_sensor1, modified_sensor2, modified_sensor3, 
                                creature.relative_x, creature.relative_y, 10*self.grid.shape[0], 10*self.grid.shape[1], creature.color, 
                                modified_food_color, 8, net, creature.species, self.constants)
            self.carnivores.append(new_creature)
    
    def _get_sensor_data_carnivore(self, grid_sensored_tiles: List[List[int]]):
        sensor_data = []
        locs = np.asarray(list(self.creature_locations.values()))
        for i in range(3): # every sensor 0 to 2
            selected_creatures = np.asarray(list(self.creature_locations.keys()))[np.where((locs[:, 0] < grid_sensored_tiles[i][0] + self.constants["carnivore_sensor_range"])
                                                                                            & (grid_sensored_tiles[i][0] - self.constants["carnivore_sensor_range"] < locs[:, 0])
                                                                                            & (locs[:, 1] < grid_sensored_tiles[i][1] + self.constants["carnivore_sensor_range"])
                                                                                            & (grid_sensored_tiles[i][1] - self.constants["carnivore_sensor_range"] < locs[:, 1]))]
            if len(selected_creatures) != 0:
                sensor_data.append([selected_creatures[0].color[0], selected_creatures[0].food, 1])
            else:
                sensor_data.append([0,0,0])
        
        return sensor_data[0], sensor_data[1], sensor_data[2]