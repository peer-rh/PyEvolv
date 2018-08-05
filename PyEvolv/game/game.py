import pygame
import numpy as np
import colorsys
from PyEvolv.assets.font import FONT, get_font

class Game:
    def __init__(self,display_width, display_height, y, grid, evo, relatives_on_screen, constants):
        self.display_width = display_width
        self.display_height = display_height
        self.relative_x = 0
        self.relative_y = 0
        self.grid = grid
        self.evo = evo
        self.constants = constants
        self.relative_x_change = 0
        self.relative_y_change = 0
        self.relatives_on_screen = relatives_on_screen
        self.y = y

        pygame.init()

        pygame.font.init()
        self.myfont = FONT

        self.clock = pygame.time.Clock()

        self.surf = pygame.Surface((display_width,display_height))
        pygame.display.set_caption('Evolution Simulator')

        self.sidebar_width = display_width-display_height
        self.map_surf = pygame.Surface((display_height, display_height))
        self.sidebar_surf = pygame.Surface((self.sidebar_width, display_height))
        self.step = 0

    def next_frame(self, creatures, creature_counts):
        self.step += self.constants["evo_steps_per_frame"]

        self.sidebar_surf.fill((255, 255, 255))
        self.map_surf.fill((0,0,0))

        self._display_grid(self.map_surf)
        self._display_creature(self.map_surf, creatures)
        self._display_sidebar(self.sidebar_surf, len(creatures), creature_counts)
        self._display_info()

        self.surf.blit(self.map_surf, (self.sidebar_width, 0))
        self.surf.blit(self.sidebar_surf, (0, 0))

        self.relative_x = min(max(0, self.relative_x + self.relative_x_change), 10*self.grid.shape[0] - self.relatives_on_screen)
        self.relative_y = min(max(0, self.relative_y + self.relative_y_change), 10*self.grid.shape[1] - self.relatives_on_screen)


    def controller(self, event):
        self._grid_controller(event)

    def update_grid(self, new_grid):
        assert new_grid.shape == self.grid.shape
        self.grid = new_grid 

    def _grid_controller(self, event):
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

    def _display_grid(self, gameDisplay):
        pixels_per_relative = self.display_height / self.relatives_on_screen
        for x in range(self.grid.shape[0]):
            for y in range(self.grid.shape[1]):
                if self.relative_x <= (x+1)*10 <= self.relative_x + self.relatives_on_screen + 10 and self.relative_y <= (y+1)*10 <= self.relative_y + self.relatives_on_screen + 10:
                    color = self.grid[x, y]
                    color = np.asarray(colorsys.hsv_to_rgb(color[0], color[1], color[2]))*255
                    pygame.draw.rect(gameDisplay, color, (x*10*pixels_per_relative - self.relative_x*pixels_per_relative, y*10*pixels_per_relative - self.relative_y*pixels_per_relative, pixels_per_relative*10, pixels_per_relative*10))
    
    def _display_creature(self, gameDisplay, creatures):
        pixels_per_relative = self.display_height / self.relatives_on_screen

        for creature in creatures:
            x, y, color, food_color, size, rotation, sensor_1, sensor_2, sensor_3 = creature()
            if self.relative_x <= x <= self.relative_x + self.relatives_on_screen and self.relative_y <= y <= self.relative_y + self.relatives_on_screen:
                size = int(size*pixels_per_relative)
                surf_size = max(size, int(self.constants["max_sensor_length"]*pixels_per_relative))

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

                dest_x = int(((x-self.relative_x)*pixels_per_relative) - (creature_surf.get_rect().width/2))
                dest_y = int(((y-self.relative_y)*pixels_per_relative) - (creature_surf.get_rect().height/2))

                gameDisplay.blit(creature_surf, (dest_x, dest_y))

    def _display_sidebar(self, gameDisplay, n_creatures, creature_counts):
        pop_size = self.myfont.render("Population: " + str(n_creatures), False, (0,0,0))
        step = self.myfont.render("Step: "+str(self.step), False, (0,0,0))
        gameDisplay.blit(pop_size, (20, 20))
        gameDisplay.blit(step, (20, 60))

        current_y = 100
        for i in creature_counts.values():
            count = i[0]
            color = i[1]
            pixels = (self.display_height-120) * (count/n_creatures)
            pygame.draw.rect(gameDisplay, np.asarray(colorsys.hsv_to_rgb(color[0], color[1], color[2]))*255,
                             (20, current_y, self.sidebar_width-40, pixels))
            current_y += pixels

    def _display_info(self):
        pos = pygame.mouse.get_pos()
        if pos[0] >= self.sidebar_width and pos[1] > self.y:
            relatives_per_pixel = self.relatives_on_screen / self.display_height
            relative_mouse_x = (pos[0] - self.sidebar_width) * relatives_per_pixel
            relative_mouse_y = (pos[1]-self.y) * relatives_per_pixel
            tile_x = int(self.relative_x//10 + relative_mouse_x // 10)
            tile_y = int(self.relative_y//10 + relative_mouse_y // 10)
            info = [np.round(self.grid[tile_x, tile_y], 2), tile_x, tile_y]

            pixels_per_relative = self.display_height / self.relatives_on_screen 

            font = get_font(int(3 * pixels_per_relative)) # add to zoom

            info_surf = pygame.Surface((pixels_per_relative*10, pixels_per_relative*10), pygame.SRCALPHA, 32)
            h_txt = font.render("h: "+str(info[0][0]), False, (0,0,0))
            s_txt = font.render("s: "+str(info[0][1]), False, (0,0,0))
            v_txt = font.render("h: "+str(info[0][2]), False, (0,0,0))
            info_surf.blit(h_txt, (pixels_per_relative, pixels_per_relative))
            info_surf.blit(s_txt, (pixels_per_relative, pixels_per_relative*4))
            info_surf.blit(v_txt, (pixels_per_relative, pixels_per_relative*7))
            self.map_surf.blit(info_surf, (tile_x*10*pixels_per_relative - self.relative_x*pixels_per_relative, tile_y*10*pixels_per_relative - self.relative_y*pixels_per_relative))

