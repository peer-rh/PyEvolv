import pygame
import numpy as np
import colorsys
import time
from typing import List, Union, Tuple
import os
from PyEvolv.grid_creator.Sidebar import Sidebar
from PyEvolv.assets.font import FONT

class GridCreator:
    def __init__(self,display_width:int, display_height:int, grid:np.ndarray, grids_path:str, relatives_on_screen:int, y:int=50, sidebar_bg:Tuple[int, int, int]=(255,255,255), sidebar_primary:Tuple[int, int, int]=(0,0,0), sidebar_secondary: Tuple[int, int, int]=(0,0,255)) -> None:
        """The GridCreator class helps with creation of grids for the Game
        
        Arguments:
            display_width {int} -- The amount of pixels the window is wide
            display_height {int} -- The amount of pixels the window is high
            grid {np.array} -- The starting grid
            relatives_on_screen {int} -- The amount of relatives displayed on the screen at the beginning
        
        Keyword Arguments:
            sidebar_bg {tuple} -- The bg color of the sidebar in RGB (default: {(255,255,255)})
            sidebar_primary {tuple} -- The primary color of the sidebar in RGB (default: {(0,0,0)})
            sidebar_secondary {tuple} -- The second primary color of the sidebar in RGB (default: {(0,0,255)})
        """

        self.display_width = display_width
        self.display_height = display_height
        self.relative_x = 0
        self.relative_y = 0
        self.grid = grid
        self.grids_path = grids_path
        self.relative_x_change = 0
        self.relative_y_change = 0
        self.relatives_on_screen = relatives_on_screen
        self.y = y

        self.font = FONT

        self.surf = pygame.Surface((display_width,display_height))
        pygame.display.set_caption('GridCreator')

        self.sidebar_width = display_width-display_height
        self.map_surf = pygame.Surface((display_height, display_height))
        self.sidebar = Sidebar(self.sidebar_width, self.display_height, self.y, background_color=sidebar_bg, primary_color=sidebar_primary, secondary_color=sidebar_secondary) 
        
        self.brush:List[Union[List[float], float]] = [[0, 0, 1], 0, 0] # color hsv, size in tiles, rel_x, rel_y
        


    def next_frame(self) -> None:
        """The next frame. Handles events and displays everything
        """
            
        self.relative_x = min(max(0, self.relative_x + self.relative_x_change), 10*self.grid.shape[0] - self.relatives_on_screen)
        self.relative_y = min(max(0, self.relative_y + self.relative_y_change), 10*self.grid.shape[1] - self.relatives_on_screen)
        
        self._sidebar_controller()
        self.sidebar.next_frame()

        self.map_surf.fill((0,0,0))

        self._display_grid(self.map_surf)

        self.surf.blit(self.map_surf, (self.sidebar_width, 0))
        self.surf.blit(self.sidebar.sidebar_surf, (0, 0))

    def controller(self, event:pygame.event) -> None:
        self.sidebar.controller(event)
        self._grid_controller(event)
        self._brush_controller(event)

    def _brush_controller(self, event:pygame.event) -> None:
        """The controller for the brush
        
        Arguments:
            event {event} -- a single event from pygame.event.get()
        """

        color_picker_used = self.sidebar.color_picker
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.sidebar_width < event.pos[0] and event.button == 1: 
                if self.sidebar.color_picker or self.sidebar.fill:
                    relatives_per_pixel = self.relatives_on_screen / self.display_height

                    relative_mouse_x = (event.pos[0] - self.sidebar_width) * relatives_per_pixel
                    relative_mouse_y = (event.pos[1]-self.y) * relatives_per_pixel
                    tile_x = int(self.relative_x//10 + relative_mouse_x // 10)
                    tile_y = int(self.relative_y//10 + relative_mouse_y // 10)
                    if self.sidebar.color_picker:
                        self.sidebar.color_picker = False
                        self.brush[0] = self.grid[tile_x, tile_y]
                        self.sidebar.update_slider(int(self.brush[0][0] * (self.sidebar_width-60)), int(self.brush[0][1] * (self.sidebar_width-60)))
                        self.grid[tile_x, tile_y] = self.brush[0]
                    
                    elif self.sidebar.fill:
                        self._flood_fill(tile_x, tile_y, list(self.grid[tile_x, tile_y]), self.brush[0])

        elif event.type == pygame.MOUSEMOTION and event.buttons[0] == 1 and not color_picker_used:
            if event.pos[0] - self.sidebar_width > 0:
                relatives_per_pixel = self.relatives_on_screen / self.display_height

                relative_mouse_x = (event.pos[0] - self.sidebar_width) * relatives_per_pixel
                relative_mouse_y = (event.pos[1]-self.y) * relatives_per_pixel

                self.brush[1] = int(self.relative_x//10 + relative_mouse_x // 10)
                self.brush[2] = int(self.relative_y//10 + relative_mouse_y // 10)
                self.grid[self.brush[1], self.brush[2]] = self.brush[0]

    def _sidebar_controller(self) -> None:
        """Connection betwenn Sidebar Class and GridCreator Class
        """

        self.brush[0][0] = self.sidebar.slider_1_val / (self.sidebar_width-60)
        self.brush[0][1] = self.sidebar.slider_1_val / (self.sidebar_width-60)

        if self.sidebar.water:
            self.brush[0] = [0, 0, 0]
        else:
            self.brush[0] = [self.sidebar.slider_1_val / (self.sidebar_width-60), self.sidebar.slider_2_val / (self.sidebar_width-60), 1]
        
        if self.sidebar.save:
            try:
                np.save(self.grids_path + self.sidebar.grid_name + ".npy", self.grid)
                self.sidebar.save = False
            except:
                pass
        if self.sidebar.load:
            try:
                np.save(self.grids_path + ".autosave.npy", self.grid)
                self.grid = np.load(self.grids_path + self.sidebar.grid_name + ".npy")
                self.sidebar.load = False
            except:
                pass
                
    def _grid_controller(self, event:pygame.event) -> None:
        """The Grid Controller to zoom and move through the grid
        
        Arguments:
            event {event} -- A single event from pygame.event.get()
        """

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


    def _display_grid(self, gameDisplay:pygame.Surface) -> None:
        """Displays the grid on the gameDisplay
        
        Arguments:
            gameDisplay {pygame.Surface} -- The surface to display the grid on
        """

        pixels_per_relative = self.display_height / self.relatives_on_screen
        for x in range(self.grid.shape[0]):
            for y in range(self.grid.shape[1]):
                if self.relative_x <= x*10 <= self.relative_x + self.relatives_on_screen and self.relative_y <= y*10 <= self.relative_y + self.relatives_on_screen:
                    color = self.grid[x, y]
                    color = np.asarray(colorsys.hsv_to_rgb(color[0], color[1], color[2]))*255
                    pygame.draw.rect(gameDisplay, (int(color[0]), int(color[1]), int(color[2])), (x*10*pixels_per_relative - self.relative_x*pixels_per_relative, y*10*pixels_per_relative - self.relative_y*pixels_per_relative, pixels_per_relative*10, pixels_per_relative*10))
    
    def _flood_fill(self, x:int, y:int, old_color:List[float], new_color:List[float]) -> None:
        """The 4flood fill algorithm
        
        Arguments:
            x {int} -- the x coordinate of the tile where the fill algo starts on
            y {int} -- the y coordinate of the tile where the fill algo starts on
            old_color {list} -- The old color of the grid tile in HSV
            new_color {list} -- The new color with which the the flooded fields should be colored in HSV
        """

        if list(self.grid[x, y]) == old_color:
            self.grid[x,y] = new_color
            self._flood_fill(x, min(self.grid.shape[1]-1, y+1), old_color, new_color)
            self._flood_fill(x, max(0, y-1), old_color, new_color)
            self._flood_fill(min(self.grid.shape[0]-1, x+1), y, old_color, new_color)
            self._flood_fill(max(0, x-1), y, old_color, new_color)