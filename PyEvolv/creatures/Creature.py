import numpy as np
from typing import Tuple, List, Dict
from PyEvolv.evolution.Net import Net

class Creature:
    def __init__(self, sensor_1:Tuple[int, int], sensor_2:Tuple[int, int], sensor_3:Tuple[int, int], relative_x:int, relative_y:int, max_x:int, max_y:int, color:Tuple[float, float, float], food_color:Tuple[float, float, float], 
                 size:int, net:Net, species:int, constants:Dict) -> None:
        """The Creature class is the object for an creature in the evolution. It takes care of converting the input from the grid to movement,
           etc and it stores its relevant information
        
        Arguments:
            sensor_1 {tuple} -- [len, degree]
            sensor_2 {tuple} -- [len, angle]
            sensor_3 {tuple} -- [len, angle]
            relative_x {int} -- the x position on the grid in relatives
            relative_y {int} -- thy y position on the grid in relatives
            max_x {int} -- the maximum x the creature can have
            max_y {int} -- the maximum y position the creature can have in relatives
            color {tuple} -- [hue, saturation, value]
            food_color {tuple} -- [hue, saturation, value]
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
        self.constants = constants
        self.dead = False

        self.get_child = False
        self.rotation = 0
        self.food = self.constants["starting_food"]
        self.steps = 0
        self.type:str = ""
        self.eat = True

        self.size_per_food = self.size/self.food
        self._update_sensor_xy()
    
    def __call__(self) -> Tuple[str, int, int, Tuple[float, float, float], Tuple[float, float, float], int, int, Tuple[int, int], Tuple[int, int], Tuple[int, int]]:
        """To get the information for drawing the creature easily
        
        Returns:
            relative_x {int} 
            relative_y {int} 
            color {tuple} 
            food_color {tuple} 
            size {int} 
            rotation {int} 
            sensor_1 {list} 
            sensor_2 {list} 
            sensor_3 {list} 

        """
        
        return self.type, self.relative_x, self.relative_y, self.color, self.food_color, self.size, self.rotation, self.sensor_1, self.sensor_2, self.sensor_3
    
    def next_step(self, food_added: float, sensor_1: List[float], sensor_2: List[float], sensor_3: List[float]) -> None:
        """The functionto let the brain think and let the creature update its value
        
        Arguments:
            food_added {float} -- The amount of food the Creature has become this step
            sensor_1 {list} -- The value on the grid where the sensor ends are [hue, saturation, value]
            sensor_2 {list} -- The value on the grid where the sensor ends are [hue, saturation, value]
            sensor_3 {list} -- The value on the grid where the sensor ends are [hue, saturation, value]
        """

        if self.food <= 0 or self.steps >= self.constants["max_lifespan"]:
            self.dead = True
        else:
            self.steps += 1
            self.food += food_added
            self.food -= self.constants["food_lost_on_step"]

            network_output = self.net(sensor_1, sensor_2, sensor_3, self.rotation, self.food) # network_output is forward_backward, left_right, rotation, get_child
            
            self.eat = network_output[3] > 0
            self.rotation = (self.rotation + network_output[1]*self.constants["degrees_creature_rotates_per_step"]) % 360
            location_change = (network_output[0]+1)/2*self.constants["relatives_creature_moves_per_step"]

            x_change = location_change * np.cos(np.radians(360-self.rotation))
            y_change = location_change * np.sin(np.radians(360-self.rotation)) # 360 - self.rotation because so no conflict with rotation in game object 
 
            self.relative_x = max(min(x_change+self.relative_x, self.max_x), 0)
            self.relative_y = max(min(y_change+self.relative_y, self.max_y), 0)
            
            self._update_sensor_xy()
            
            if self.food >= self.constants["food_lost_on_new_child"] + 2 and network_output[2] > 0:
                self.get_child = True
            self._update_size()

    def _update_size(self) -> None:
        """Simple size updater, which updates the size according to its current food
        """

        self.size = max(0, min(self.constants["max_creature_size"], int(self.food*self.size_per_food)))
    
    def _update_sensor_xy(self):
        self.sensor_1_x = int(self.sensor_1[0]*np.cos(np.radians(self.sensor_1[1]+self.rotation)))
        self.sensor_1_y = int(self.sensor_1[0]*np.sin(np.radians(self.sensor_1[1]+self.rotation)))
        self.sensor_2_x = int(self.sensor_2[0]*np.cos(np.radians(self.sensor_2[1]+self.rotation)))
        self.sensor_2_y = int(self.sensor_2[0]*np.sin(np.radians(self.sensor_2[1]+self.rotation)))
        self.sensor_3_x = int(self.sensor_3[0]*np.cos(np.radians(self.sensor_3[1]+self.rotation)))
        self.sensor_3_y = int(self.sensor_3[0]*np.sin(np.radians(self.sensor_3[1]+self.rotation)))

        self.grid_sensored_tiles = [[self.relative_x + self.sensor_1_x, self.relative_y + self.sensor_1_y],
                                   [self.relative_x + self.sensor_2_x, self.relative_y + self.sensor_2_y],
                                   [self.relative_x + self.sensor_3_x, self.relative_y + self.sensor_3_y]]



        