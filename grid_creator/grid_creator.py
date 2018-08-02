import pygame
import numpy as np
import colorsys
import time
from Sidebar import Sidebar

class Game:
    def __init__(self,display_width, display_height, grid, relatives_on_screen, sidebar_bg=(255,255,255), sidebar_primary=(0,0,0), sidebar_primary2=(0,0,255)):
        self.display_width = display_width
        self.display_height = display_height
        self.relative_x = 0
        self.relative_y = 0
        self.grid = grid
        self.relative_x_change = 0
        self.relative_y_change = 0
        self.relatives_on_screen = relatives_on_screen

        pygame.init()
        
        pygame.font.init()
        self.myfont = pygame.font.Font('../Arial.ttf', 20)
        
        self.clock = pygame.time.Clock()

        self.gameDisplay = pygame.display.set_mode((display_width,display_height))
        pygame.display.set_caption('GridCreator')

        self.sidebar_width = display_width-display_height
        self.map_surf = pygame.Surface((display_height, display_height))
        self.sidebar = Sidebar(self.sidebar_width, self.display_height, background_color=sidebar_bg, primary_color=sidebar_primary, primary_color_2=sidebar_primary2) 
        self.crashed = False
        
        self.brush = [[0, 0, 1], 0, 0] # color hsv, size in tiles, rel_x, rel_y


    def next_frame(self):
        if not self.crashed:
            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    self.crashed = True
                self.sidebar.controller(event)
                self._grid_controller(event)
                self._brush_controller(event)
            
            self.relative_x = min(max(0, self.relative_x + self.relative_x_change), 10*self.grid.shape[0] - self.relatives_on_screen)
            self.relative_y = min(max(0, self.relative_y + self.relative_y_change), 10*self.grid.shape[1] - self.relatives_on_screen)
            
            self._sidebar_controller()
            self.sidebar.next_frame()

            self.map_surf.fill((0,0,0))

            self._display_grid(self.map_surf)

            self.gameDisplay.blit(self.map_surf, (self.sidebar_width, 0))
            self.gameDisplay.blit(self.sidebar.sidebar_surf, (0, 0))

            pygame.display.update()
            self.clock.tick(60)

    def _brush_controller(self, event):
        color_picker_used = self.sidebar.color_picker
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.sidebar_width < event.pos[0] and event.button == 1: 
                if self.sidebar.color_picker or self.sidebar.fill:
                    relatives_per_pixel = self.relatives_on_screen / self.display_height

                    relative_mouse_x = (event.pos[0] - self.sidebar_width) * relatives_per_pixel
                    relative_mouse_y = event.pos[1] * relatives_per_pixel
                    tile_x = int(self.relative_x//10 + relative_mouse_x // 10)
                    tile_y = int(self.relative_y//10 + relative_mouse_y // 10)
                    if self.sidebar.color_picker:
                        self.sidebar.color_picker = False
                        self.brush[0] = self.grid[tile_x, tile_y]
                        self.sidebar.update_slider(self.brush[0][0] * (self.sidebar_width-60), self.brush[0][1] * (self.sidebar_width-60))
                        self.grid[tile_x, tile_y] = self.brush[0]
                    
                    elif self.sidebar.fill:
                        self._flood_fill(tile_x, tile_y, list(self.grid[tile_x, tile_y]), self.brush[0])

        elif event.type == pygame.MOUSEMOTION and event.buttons[0] == 1 and not color_picker_used:
            if event.pos[0] - self.sidebar_width > 0:
                relatives_per_pixel = self.relatives_on_screen / self.display_height

                relative_mouse_x = (event.pos[0] - self.sidebar_width) * relatives_per_pixel
                relative_mouse_y = event.pos[1] * relatives_per_pixel

                self.brush[1] = int(self.relative_x//10 + relative_mouse_x // 10)
                self.brush[2] = int(self.relative_y//10 + relative_mouse_y // 10)
                self.grid[self.brush[1], self.brush[2]] = self.brush[0]

    def _sidebar_controller(self):
        self.brush[0][0] = self.sidebar.slider_1_val / (self.sidebar_width-60)
        self.brush[0][1] = self.sidebar.slider_1_val / (self.sidebar_width-60)

        if self.sidebar.water:
            self.brush[0] = [0, 0, 0]
        else:
            self.brush[0] = [self.sidebar.slider_1_val / (self.sidebar_width-60), self.sidebar.slider_2_val / (self.sidebar_width-60), 1]
        
        if self.sidebar.save:
            try:
                np.save("../grids/" + self.sidebar.grid_name + ".npy", self.grid)
                self.sidebar.save = False
            except:
                print("failed")
        if self.sidebar.load:
            try:
                np.save("../grids/.autosave.npy", self.grid)
                self.grid = np.load("../grids/" + self.sidebar.grid_name + ".npy")
                self.sidebar.load = False
            except:
                print("failed")
    
    def _grid_controller(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.relative_x_change = -5
            elif event.key == pygame.K_RIGHT:
                self.relative_x_change = 5
            
            if event.key == pygame.K_DOWN:
                self.relative_y_change = 5
        
            elif event.key == pygame.K_UP:
                self.relative_y_change = -5

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                self.relative_x_change = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                self.relative_y_change = 0
    
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
                self.relatives_on_screen = min(max(10, self.relatives_on_screen + 6), self.grid.shape[0]*10)
            elif event.button == 5:
                self.relatives_on_screen = min(max(10, self.relatives_on_screen - 6), self.grid.shape[0]*10)


    def _display_grid(self, gameDisplay):
        pixels_per_relative = self.display_height / self.relatives_on_screen
        for x in range(self.grid.shape[0]):
            for y in range(self.grid.shape[1]):
                color = self.grid[x, y]
                color = np.asarray(colorsys.hsv_to_rgb(color[0], color[1], color[2]))*255
                pygame.draw.rect(gameDisplay, (int(color[0]), int(color[1]), int(color[2])), (x*10*pixels_per_relative - self.relative_x*pixels_per_relative, y*10*pixels_per_relative - self.relative_y*pixels_per_relative, pixels_per_relative*10, pixels_per_relative*10))
    
    def _flood_fill(self, x, y, old_color, new_color):
        if list(self.grid[x, y]) == old_color:
            self.grid[x,y] = new_color
            self._flood_fill(x, min(self.grid.shape[1]-1, y+1), old_color, new_color)
            self._flood_fill(x, max(0, y-1), old_color, new_color)
            self._flood_fill(min(self.grid.shape[0]-1, x+1), y, old_color, new_color)
            self._flood_fill(max(0, x-1), y, old_color, new_color)


gc = Game(800, 600,np.zeros((75, 75, 3)), 750)
while not gc.crashed:
    gc.next_frame()

np.save(".autosave.npy", gc.grid)