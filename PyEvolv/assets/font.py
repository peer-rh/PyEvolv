import pygame
import PyEvolv
import os

pygame.font.init()
path = os.path.join(PyEvolv.__path__[0], 'assets', 'Arial.ttf')
FONT = pygame.font.Font(path, 20)

def get_font(size):
    return pygame.font.Font(path, size)

