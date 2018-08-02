import numpy as np
from CONSTANTS import *


class Creature:
    def __init__(self, sensor_1, sensor_2, sensor_3, relative_x, relative_y, max_x, max_y, color, food_color, size, net, species):
        """The Creature class is the object for an creature in the evolution. It takes care of converting the input from the grid to movement,
           etc and it stores its relevant information
        
        Arguments:
            sensor_1 {list} -- [len, degree]
            sensor_2 {list} -- [len, angle]
            sensor_3 {list} -- [len, angle]
            relative_x {int} -- the x position on the grid in relatives
            relative_y {int} -- thy y position on the grid in relatives
            max_x {int} -- the maximum x the creature can have
            max_y {int} -- the maximum y position the creature can have in relatives
            color {list} -- [hue, saturation, value]
            food_color {list} -- [hue, saturation, value]
            size {int} -- the starting size it has
            net {Net} -- the Net class which is the brain of the creature
            species {int} -- Its species value
        """

        self.color = color
        self.food_color = food_color
        self.size = size
        self.net = net
        self.relative_x = relative_x
        self.relative_y = relative_y
        self.max_x = max_x
        self.max_y = max_y
        self.species = species
        self.sensor_1, self.sensor_2, self.sensor_3 = sensor_1, sensor_2, sensor_3
        self.sensor_1_x = int(sensor_1[0]*np.cos(sensor_1[1]))
        self.sensor_1_y = int(sensor_1[0]*np.sin(sensor_1[1]))
        self.sensor_2_x = int(sensor_2[0]*np.cos(sensor_2[1]))
        self.sensor_2_y = int(sensor_2[0]*np.sin(sensor_2[1]))
        self.sensor_3_x = int(sensor_3[0]*np.cos(sensor_3[1]))
        self.sensor_3_y = int(sensor_3[0]*np.sin(sensor_3[1]))
        self.dead = False

        self.get_child = False
        self.rotation = 0
        self.food = STARTING_FOOD
        self.steps = 0

        self.size_per_food = self.size/self.food
        self.grid_sensored_tiles = [[self.relative_x + self.sensor_1_x, self.relative_y + self.sensor_1_y],
                                   [self.relative_x + self.sensor_2_x, self.relative_y + self.sensor_2_y],
                                   [self.relative_x + self.sensor_3_x, self.relative_y + self.sensor_3_y]]
    
    def __call__(self):
        """To get the information for drawing the creature easily
        
        Returns:
            relative_x {int} 
            relative_y {int} 
            color {list} 
            food_color {list} 
            size {int} 
            rotation {int} 
            sensor_1 {list} 
            sensor_2 {list} 
            sensor_3 {list} 

       """

        return self.relative_x, self.relative_y, self.color, self.food_color, self.size, self.rotation, self.sensor_1, self.sensor_2, self.sensor_3
    
    def next_step(self, food_added, sensor_1, sensor_2, sensor_3):
        """The functionto let the brain think and let the creature update its value
        
        Arguments:
            food_added {float} -- The amount of food the Creature has become this step
            sensor_1 {list} -- The value on the grid where the sensor ends are [hue, saturation, value]
            sensor_2 {list} -- The value on the grid where the sensor ends are [hue, saturation, value]
            sensor_3 {list} -- The value on the grid where the sensor ends are [hue, saturation, value]
        """

        if self.food <= 0 or self.steps >= MAX_LIFESPAN:
            self.dead = True
        else:
            self.steps += 1
            self.food += food_added
            self.food -= FOOD_LOST_ON_STEP

            out = self.net(sensor_1, sensor_2, sensor_3, self.rotation, self.food) # out is forward_backward, left_right, rotation
            
            self.relative_x = max(min(out[0]*RELATIVES_CREATURE_MOVES_PER_STEP+self.relative_x, self.max_x), 0)
            self.relative_y = max(min(out[1]*RELATIVES_CREATURE_MOVES_PER_STEP+self.relative_y, self.max_y), 0)
            self.rotation = (self.rotation + out[2]*DEGREES_CREATURE_ROTATES_PER_STEP) % 360
            
            # TODO: Come up with better name
            self.grid_sensored_tiles = [[self.relative_x + self.sensor_1_x, self.relative_y + self.sensor_1_y],
                                    [self.relative_x + self.sensor_2_x, self.relative_y + self.sensor_2_y],
                                    [self.relative_x + self.sensor_3_x, self.relative_y + self.sensor_3_y]]
            
            if self.food >= FOOD_LOST_ON_NEW_CHILD + 2 and out[3] > 0:
                self.get_child = True
            self._update_size()

    def _update_size(self):
        """Simple size updater, which updates the size according to its current food
        """

        self.size = max(0, min(MAX_CREATURE_SIZE, int(self.food*self.size_per_food)))



        