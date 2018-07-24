import numpy as np

# Maybe upgrade to tensorflow or nupic or keras

class Net:
    def __init__(self, weights):
        self.weights = weights
    
    def __call__(self, sensor_1, sensor_2, sensor_3, rotation, food):
        inputs = np.array([*sensor_1, *sensor_2, *sensor_3, rotation, food])
        out = np.tanh(np.dot(inputs, self.weights))
        return out