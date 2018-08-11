import numpy as np
import copy
from typing import List

# Maybe upgrade to tensorflow or nupic or keras

class Net:
    def __init__(self, n_hidden_units, parents:List=[], min_weight_mutation:int=-0.01, max_weight_mutation:int=0.01) -> None:
        """A simple 2 layer network with the tanh activation function
        
        Arguments:
            weights_1 {np.array} -- connections between (input, hidden_state) and hidden layer
            weights_2 {np.array} -- connections between hidden layer and output
        """
        if len(parents) == 0:
            self.weights = {
                "w1": np.random.randn(n_hidden_units+11, n_hidden_units)*0.3,
                "w2": np.random.randn(n_hidden_units, n_hidden_units)*0.3,
                "w3": np.random.randn(n_hidden_units, 4)*0.2 # forward, rotation, get_child, eat
            }
        else: # crossover and mutation
            self.weights = {
                "w1": np.array([[parents[parent_picked].weights["w1"][i][j] for j, parent_picked in enumerate(np.random.randint(0, len(parents), n_hidden_units))] for i in range(n_hidden_units+11)]),
                "w2": np.array([[parents[parent_picked].weights["w2"][i][j] for j, parent_picked in enumerate(np.random.randint(0, len(parents), n_hidden_units))] for i in range(n_hidden_units)]),
                "w3": np.array([[parents[parent_picked].weights["w3"][i][j] for j, parent_picked in enumerate(np.random.randint(0, len(parents), 4))] for i in range(n_hidden_units)])
            }
            self.weights = {key: val+np.random.uniform(min_weight_mutation, max_weight_mutation, val.shape) for key, val in self.weights.items()}
        self.hidden_state = np.zeros(n_hidden_units)

    
    def __call__(self, sensor_1: List[float], sensor_2: List[float], sensor_3: List[float], rotation:int, food:float) -> np.ndarray:
        """The function to feed forward input through the Neural Net
        
        Arguments:
            sensor_1 {list} -- The value of sensor_1 on the grid
            sensor_2 {list} -- The value of sensor_2 on the grid
            sensor_3 {list} -- The value of sensor_3 on the grid
            rotation {int} -- the curent rotation of the creature
            food {float} -- the current amount of food the creature has
        
        Returns:
            np.array -- the output of the network
        """

        inputs = np.array([*self.hidden_state, *sensor_1, *sensor_2, *sensor_3, rotation, food])
        out = np.tanh(np.dot(inputs, self.weights["w1"]))
        out = np.tanh(np.dot(out, self.weights["w2"]))
        self.hidden_state = out
        out = np.tanh(np.dot(out, self.weights["w3"]))
        return out