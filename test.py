import pygame
import numpy as np

sensor_1 = 20, 20.0
sensor_2 = 20, 340.0
sensor_3 = 20, 360

sensor_3_x = sensor_3[0]*np.cos(np.radians(float(sensor_3[1])))
sensor_3_y = sensor_3[0]*np.sin(np.radians(float(sensor_3[1])))
print(sensor_3_x, sensor_3_y)
print(np.cos(np.radians(90)))

pygame.init()
gameDisplay = pygame.display.set_mode((400, 400))

while True:
    gameDisplay.fill((255, 255, 255))
    pygame.event.get()
    pygame.draw.line(gameDisplay, (0,0,0), (200, 200), (int(sensor_3_x+200), int(sensor_3_y+200)))
    pygame.display.update()