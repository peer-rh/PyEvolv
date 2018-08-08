import numpy as np
from typing import List

# Maybe upgrade to tensorflow or nupic or keras

class Net:
    def __init__(self, weights_1: np.ndarray, weights_2: np.ndarray, weights_3: np.ndarray) -> None:
        """A simple 2 layer network with the tanh activation function
        
        Arguments:
            weights_1 {np.array} -- connections between (input, hidden_state) and hidden layer
            weights_2 {np.array} -- connections between hidden layer and output
        """

        self.weights_1 = weights_1
        self.weights_2 = weights_2
        self.weights_3 = weights_3
        self.hidden_state = np.zeros(self.weights_1.shape[1])
    
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
        out = np.tanh(np.dot(inputs, self.weights_1))
        out = np.tanh(np.dot(out, self.weights_2))
        self.hidden_state = out
        out = np.tanh(np.dot(out, self.weights_3))
        return out