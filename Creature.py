import numpy as np
from CONSTANTS import *


class Creature:
    def __init__(self, sensor_1, sensor_2, sensor_3, relative_x, relative_y, max_x, max_y, color, food_color, size, net):
        self.color = color
        self.food_color = food_color
        self.size = size
        self.net = net
        self.relative_x = relative_x
        self.relative_y = relative_y
        self.max_x = max_x
        self.max_y = max_y
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
        self.food = 100
        self.steps = 0

        self.size_per_food = self.size/self.food
        self.grid_sensored_tiles = [[self.relative_x + self.sensor_1_x, self.relative_y + self.sensor_1_y],
                                   [self.relative_x + self.sensor_2_x, self.relative_y + self.sensor_2_y],
                                   [self.relative_x + self.sensor_3_x, self.relative_y + self.sensor_3_y]]
    
    def __call__(self):
        return self.relative_x, self.relative_y, self.color, self.food_color, self.size, self.rotation, self.sensor_1, self.sensor_2, self.sensor_3
    
    def next_step(self, food_added, sensor_1, sensor_2, sensor_3):
        if self.food <= 0:
            self.dead = True
        else:
            self.steps += 1
            self.food += food_added
            self.food -= FOOD_LOST_ON_STEP

            out = self.net(sensor_1, sensor_2, sensor_3, self.rotation, self.food) # out is forward_backward, left_right, rotation
            
            self.relative_y = max(min(RELATIVES_CREATURE_MOVES_PER_STEP+self.relative_x, self.max_x), 0)
            self.relative_x = max(min(RELATIVES_CREATURE_MOVES_PER_STEP+self.relative_y, self.max_y), 0)
            self.rotation = (self.rotation + out[2]*DEGREES_CREATURE_ROTATES_PER_STEP) % 360
            print(self, self.relative_x, self.relative_y, self.food)
            
            # TODO: Come up with better name
            self.grid_sensored_tiles = [[self.relative_x + self.sensor_1_x, self.relative_y + self.sensor_1_y],
                                    [self.relative_x + self.sensor_2_x, self.relative_y + self.sensor_2_y],
                                    [self.relative_x + self.sensor_3_x, self.relative_y + self.sensor_3_y]]
            
            if self.food >= 20 and out[3] > 0:
                self.get_child = True
       # self._update_size()

    #def _update_size(self):
    #    self.size = int(self.food*self.size_per_food)



        