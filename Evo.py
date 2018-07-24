import numpy as np

from CONSTANTS import *
from Creature import Creature
from Net import Net

class Evolution():
    def __init__(self, n_population, grid):
        self.n_population = n_population
        self.grid = grid
        self._create_population()
        
    def next_step(self):
        self.grid += 2

        for creature in self.creatures:
            if creature.dead:
                self.creatures.remove(creature)
            else:
                food_added = self._calculate_food_added(creature)
                sensor_1 = self.grid[min(self.grid.shape[0]-1, int(creature.grid_sensored_tiles[0][0]/10)), min(self.grid.shape[1]-1, int(creature.grid_sensored_tiles[0][1]/10))]
                sensor_2 = self.grid[min(self.grid.shape[0]-1, int(creature.grid_sensored_tiles[1][0]/10)), min(self.grid.shape[1]-1, int(creature.grid_sensored_tiles[1][1]/10))]
                sensor_3 = self.grid[min(self.grid.shape[0]-1, int(creature.grid_sensored_tiles[2][0]/10)), min(self.grid.shape[1]-1, int(creature.grid_sensored_tiles[2][1]/10))]


                self.grid[:,:,:3] = np.minimum(255, self.grid[:,:,:3]+FOOD_ADDED_PER_STEP)

                creature.next_step(food_added, sensor_1, sensor_2, sensor_3)
        for creature in self.creatures:
             if creature.get_child and len(self.creatures) < MAX_POPULATION:
                    self._create_new_child(creature)
            
        self.grid = np.maximum(0, np.minimum(255, self.grid))


    def _create_population(self):
        self.creatures = []
        for _ in range(self.n_population):
            weights = np.random.randn(11, 4)*0.001
            net = Net(weights)
            sensors = np.concatenate([np.random.randint(0, MAX_SENSOR_LENGTH, (3)),
                                      np.random.randint(0, 360, 3)])

            x = np.random.randint(0, 10*self.grid.shape[0])
            y = np.random.randint(0, 10*self.grid.shape[1])
            color = np.random.randint(0, 255, 3)
            food_color = (255, 255, 255)
            size = STARTING_SIZE
            self.creatures.append(Creature(sensors[:2], sensors[2:4], sensors[4:6], x, y, self.grid.shape[0], self.grid.shape[1], color, food_color, size, net))
    
    def _calculate_food_added(self, creature):
        x, y = creature.relative_x, creature.relative_y
        food_preference = creature.food_color
        tile = self.grid[min(self.grid.shape[0]-1, int(x/10)), min(self.grid.shape[0]-1, int(y/10))]
        difference = np.sum(np.abs(food_preference - tile))
        food_given = MAX_FOOD_DIFFERNCE_FOR_NO_LOSS - difference
        food_given = max(-MAX_FOOD_LOSS, food_given)
        self.grid[min(self.grid.shape[0]-1, int(x/10)), min(self.grid.shape[0]-1, int(y/10))] -= int(food_given/3)
        # Probably Bug making Black liking best as can jst stay there # TODO: Observe if used and later delete bug
        return food_given
    
    def _create_new_child(self, creature):
        creature.food -= 18
        modification_matrix = np.random.uniform(MIN_WEIGHT_MUTATION, MAX_WEIGHT_MUTATION, (11, 4))
        modified_weights = creature.net.weights + modification_matrix
        modified_color = [max(0, min(255, i)) for i in creature.color + np.random.randint(MIN_COLOR_CHANGE, MAX_COLOR_CHANGE, 3)]
        modified_food_color = [max(0, min(255, i)) for i in creature.food_color + np.random.randint(MIN_COLOR_CHANGE, MAX_COLOR_CHANGE, 3)]
        modified_sensor1 = (min(MAX_SENSOR_LENGTH, creature.sensor_1[0]+np.random.randint(MIN_SENSOR_LEN_MUTATION, MAX_SENSOR_ANGLE_MUTATION)),
                            creature.sensor_1[1] + np.random.randint(MIN_SENSOR_ANGLE_MUTATION, MAX_SENSOR_ANGLE_MUTATION) % 360)
        modified_sensor2 = (min(MAX_SENSOR_LENGTH, creature.sensor_2[0]+np.random.randint(MIN_SENSOR_LEN_MUTATION, MAX_SENSOR_ANGLE_MUTATION)),
                            creature.sensor_2[1] + np.random.randint(MIN_SENSOR_ANGLE_MUTATION, MAX_SENSOR_ANGLE_MUTATION) % 360)
        modified_sensor3 = (min(MAX_SENSOR_LENGTH, creature.sensor_3[0]+np.random.randint(MIN_SENSOR_LEN_MUTATION, MAX_SENSOR_ANGLE_MUTATION)),
                            creature.sensor_3[1] + np.random.randint(MIN_SENSOR_ANGLE_MUTATION, MAX_SENSOR_ANGLE_MUTATION) % 360)
        
        net = Net(modified_weights)
        new_creature = Creature(modified_sensor1, modified_sensor2, modified_sensor3, 
                                creature.relative_x, creature.relative_y, self.grid.shape[0], self.grid.shape[1], modified_color, 
                                modified_food_color, 8, net)
        self.creatures.append(new_creature)