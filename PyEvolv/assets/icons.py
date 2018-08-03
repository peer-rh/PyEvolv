import cv2
import os
import PyEvolv

path = os.path.join(PyEvolv.__path__[0], 'assets', 'water.png')
WATER_IMG = cv2.imread(path, cv2.IMREAD_UNCHANGED)

path = os.path.join(PyEvolv.__path__[0], 'assets', 'fill_bucket.png')
FILL_IMG = cv2.imread(path, cv2.IMREAD_UNCHANGED)

path = os.path.join(PyEvolv.__path__[0], 'assets', 'color_picker.png')
COLOR_PICKER_IMG = cv2.imread(path, cv2.IMREAD_UNCHANGED)
