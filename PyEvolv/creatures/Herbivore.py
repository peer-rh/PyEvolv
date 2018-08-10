from PyEvolv.creatures.Creature import Creature
from typing import Tuple, List, Dict
from PyEvolv.evolution.Net import Net

class Herbivore(Creature):
    def __init__(self,sensor_1:Tuple[int, int], sensor_2:Tuple[int, int], sensor_3:Tuple[int, int], relative_x:int, relative_y:int, max_x:int, max_y:int, color:Tuple[float, float, float], 
                food_color:Tuple[float, float, float], size:int, net:Net, species:int, constants:Dict):

        super(Herbivore, self).__init__(sensor_1, sensor_2, sensor_3, relative_x, relative_y, max_x, max_y, color, food_color, size, net, species, constants)
        self.type = "Herbivore"
