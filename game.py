import pygame
import numpy as np
from Creature import Creature
import colorsys
from CONSTANTS import *

class Game:
    def __init__(self,display_width, display_height, grid, evo, relatives_on_screen):
        self.display_width = display_width
        self.display_height = display_height
        self.relative_x = 0
        self.relative_y = 0
        self.grid = grid
        self.evo = evo
        self.relative_x_change = 0
        self.relative_y_change = 0
        self.relatives_on_screen = relatives_on_screen

        pygame.init()

        pygame.font.init()
        self.myfont = pygame.font.Font("Arial.ttf", 20)

        self.clock = pygame.time.Clock()

        self.gameDisplay = pygame.display.set_mode((display_width,display_height))
        pygame.display.set_caption('Evolution Simulator')

        self.sidebar_width = display_width-display_height
        self.map_surf = pygame.Surface((display_height, display_height))
        self.sidebar_surf = pygame.Surface((self.sidebar_width, display_height))
        self.crashed = False
        self.step = 0

    def next_frame(self, creatures, creature_counts):
        if not self.crashed:
            self.step += EVO_STEPS_PER_FRAME
            events = pygame.event.get()
            self._grid_controller(events)
            for event in events:
                if event.type == pygame.QUIT:
                    self.crashed = True

            self.sidebar_surf.fill((255, 255, 255))
            self.map_surf.fill((0,0,0))

            self._display_grid(self.map_surf)
            self._display_creature(self.map_surf, creatures)
            self._display_sidebar(self.sidebar_surf, len(creatures), creature_counts)


            self.gameDisplay.blit(self.map_surf, (self.sidebar_width, 0))
            self.gameDisplay.blit(self.sidebar_surf, (0, 0))

            pygame.display.update()
    
    def update_grid(self, new_grid):
        assert new_grid.shape == self.grid.shape
        self.grid = new_grid 

    def _grid_controller(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.relative_x_change = -3
                elif event.key == pygame.K_RIGHT:
                    self.relative_x_change = 3
                
                if event.key == pygame.K_DOWN:
                    self.relative_y_change = 3
            
                elif event.key == pygame.K_UP:
                    self.relative_y_change = -3

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    self.relative_x_change = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    self.relative_y_change = 0
        
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    self.relatives_on_screen = min(max(10, self.relatives_on_screen + 3), self.grid.shape[0]*10)
                elif event.button == 5:
                    self.relatives_on_screen = min(max(10, self.relatives_on_screen - 3), self.grid.shape[0]*10)

        
        self.relative_x = min(max(0, self.relative_x + self.relative_x_change), 10*self.grid.shape[0] - self.relatives_on_screen)
        self.relative_y = min(max(0, self.relative_y + self.relative_y_change), 10*self.grid.shape[1] - self.relatives_on_screen)

    def _display_grid(self, gameDisplay):
        pixels_per_relative = self.display_height / self.relatives_on_screen
        for x in range(self.grid.shape[0]):
            for y in range(self.grid.shape[1]):
                color = self.grid[x, y]
                color = np.asarray(colorsys.hsv_to_rgb(color[0], color[1], color[2]))*255
                pygame.draw.rect(gameDisplay, color, (x*10*pixels_per_relative - self.relative_x*pixels_per_relative, y*10*pixels_per_relative - self.relative_y*pixels_per_relative, pixels_per_relative*10, pixels_per_relative*10))
    
    def _display_creature(self, gameDisplay, creatures):
        pixels_per_relative = self.display_height / self.relatives_on_screen

        for creature in creatures:
            x, y, color, food_color, size, rotation, sensor_1, sensor_2, sensor_3 = creature()
            if self.relative_x <= x <= self.relative_x + self.relatives_on_screen and self.relative_y <= y <= self.relative_y + self.relatives_on_screen:
                size = int(size*pixels_per_relative)
                surf_size = max(size, int(MAX_SENSOR_LENGTH*pixels_per_relative))

                creature_surf = pygame.Surface((2*surf_size, 2*surf_size), pygame.SRCALPHA, 32)
                creature_surf = creature_surf.convert_alpha()

            
                color = np.asarray(colorsys.hsv_to_rgb(color[0], color[1], color[2]))*255
                food_color = np.asarray(colorsys.hsv_to_rgb(food_color[0], food_color[1], food_color[2]))*255 

                pygame.draw.circle(creature_surf, color, (surf_size, surf_size), size)
                pygame.draw.circle(creature_surf, food_color, (surf_size, surf_size- size//2), size//2)

                pygame.draw.line(creature_surf, (0,0,0), (surf_size, surf_size), (surf_size - pixels_per_relative * int(sensor_1[0]*np.cos(sensor_1[1])), surf_size - pixels_per_relative * int(sensor_1[0]*np.sin(sensor_1[1]))))
                pygame.draw.line(creature_surf, (0,0,0), (surf_size, surf_size), (surf_size - pixels_per_relative * int(sensor_2[0]*np.cos(sensor_2[1])), surf_size - pixels_per_relative * int(sensor_2[0]*np.sin(sensor_2[1]))))
                pygame.draw.line(creature_surf, (0,0,0), (surf_size, surf_size), (surf_size - pixels_per_relative * int(sensor_3[0]*np.cos(sensor_3[1])), surf_size - pixels_per_relative * int(sensor_3[0]*np.sin(sensor_3[1]))))

                creature_surf = pygame.transform.rotate(creature_surf, rotation)
                creature_surf.get_rect().center = (x,y)
                gameDisplay.blit(creature_surf, ((x - self.relative_x)*pixels_per_relative - surf_size, (y - self.relative_y)*pixels_per_relative - surf_size))

    def _display_sidebar(self, gameDisplay, n_creatures, creature_counts):
        pop_size = self.myfont.render("Population: " + str(n_creatures), False, (0,0,0))
        step = self.myfont.render("Step: "+str(self.step), False, (0,0,0))
        gameDisplay.blit(pop_size, (20, 20))
        gameDisplay.blit(step, (20, 60))

        current_y = 100
        for i in creature_counts.values():
            count = i[0]
            color = i[1]
            pixels = 400 * (count/n_creatures)
            pygame.draw.rect(gameDisplay, np.asarray(colorsys.hsv_to_rgb(color[0], color[1], color[2]))*255,
                             (20, current_y, self.sidebar_width-40, pixels))
            current_y += pixels
