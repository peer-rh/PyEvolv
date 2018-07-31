import numpy as np

# Maybe upgrade to tensorflow or nupic or keras

class Net:
    def __init__(self, weights_1, weights_2):
        self.weights_1 = weights_1
        self.weights_2 = weights_2
    
    def __call__(self, sensor_1, sensor_2, sensor_3, rotation, food):
        inputs = np.array([*sensor_1, *sensor_2, *sensor_3, rotation, food])
        out = np.tanh(np.dot(inputs, self.weights_1))
        out = np.tanh(np.dot(out, self.weights_2))
        return out