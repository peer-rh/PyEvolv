import pygame
import numpy as np
import colorsys
import time

class Game:
    def __init__(self,display_width, display_height, grid, relatives_on_screen):
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
        self.sidebar_surf = pygame.Surface((self.sidebar_width, display_height))
        self.crashed = False

        self.water = False
        self.color_picker = [0,0,0]
        self.color_picker_on = False
        self.fill = False
        self.brush = [[0, 0, 1], 1, 0, 0] # color hsv, size in tiles, rel_x, rel_y

        self.slider_1_value = 0
        self.slider_2_value = 0

    def next_frame(self):
        if not self.crashed:
            events = pygame.event.get()
            self._grid_controller(events)
            self._brush_controller(events)
            self._sidebar_controller(events)
            for event in events:
                if event.type == pygame.QUIT:
                    self.crashed = True

            self.sidebar_surf.fill((255, 255, 255))
            self.map_surf.fill((0,0,0))

            self._display_grid(self.map_surf)
            self._draw_sidebar(self.sidebar_surf)

            self.gameDisplay.blit(self.map_surf, (self.sidebar_width, 0))
            self.gameDisplay.blit(self.sidebar_surf, (0, 0))

            pygame.display.update()

    def _brush_controller(self, events):
        for event in events:
            if event.type == pygame.MOUSEMOTION:
                if event.pos[0] - self.sidebar_width > 0 and not self.fill:
                    relatives_per_pixel = self.relatives_on_screen / self.display_height

                    relative_mouse_x = (event.pos[0] - self.sidebar_width) * relatives_per_pixel
                    relative_mouse_y = event.pos[1] * relatives_per_pixel

                    self.brush[2] = int(self.relative_x//10 + relative_mouse_x // 10)
                    self.brush[3] = int(self.relative_y//10 + relative_mouse_y // 10)
                    if event.buttons[0] == 1:
                        self.grid[self.brush[2], self.brush[3]] = self.brush[0]

    def _sidebar_controller(self, events):
        for event in events:
            if event.type == pygame.MOUSEMOTION:
                if 20 <= event.pos[0] <= self.sidebar_width - 40 and 20 < event.pos[1] < 40 and event.buttons[0] == 1:
                    self.slider_1_value = event.pos[0] - 20
                    self.brush[0][0] = self.slider_1_value / (self.sidebar_width-60)

                if 20 <= event.pos[0] <= self.sidebar_width - 40 and 60 < event.pos[1] < 80 and event.buttons[0] == 1:
                    self.slider_2_value = event.pos[0] - 20
                    self.brush[0][1] = self.slider_2_value / (self.sidebar_width-60)

            if event.type == pygame.MOUSEBUTTONDOWN:                
                pos = pygame.mouse.get_pos()
                if not self.color_picker_on:
                    if 20 <= pos[0] <= self.sidebar_width - 20 and 100 < pos[1] < 120 and event.button == 1:
                        if not self.water:
                            self.water = True
                            self.brush[0] = [0, 0, 0]
                            self.slider_1_value = 0
                            self.slider_2_value = 0
                        else:
                            self.water = False
                            self.brush[0] = [0, 0, 1]
                            self.slider_1_value = 0
                            self.slider_2_value = 0
                    elif 20 <= pos[0] <= self.sidebar_width - 20 and 140 < pos[1] < 185 and event.button == 1:
                        self.color_picker_on = True
                    elif 20 <= pos[0] <= self.sidebar_width - 20 and 200 < pos[1] < 220 and event.button == 1:
                        if self.fill:
                            self.fill = False
                        else:
                            self.fill = True
                else:
                    if self.sidebar_width < pos[0] and event.button == 1: 
                        relatives_per_pixel = self.relatives_on_screen / self.display_height

                        relative_mouse_x = (event.pos[0] - self.sidebar_width) * relatives_per_pixel
                        relative_mouse_y = event.pos[1] * relatives_per_pixel
                        tile_x = int(self.relative_x//10 + relative_mouse_x // 10)
                        tile_y = int(self.relative_y//10 + relative_mouse_y // 10)

                        self.color_picker = self.grid[tile_x, tile_y]
                        self.brush[0] = self.color_picker
                        self.slider_1_value = self.color_picker[0] * (self.sidebar_width-60)
                        self.slider_2_value = self.color_picker[1] * (self.sidebar_width-60)
                        self.color_picker_on = False
                if self.fill:
                    if self.sidebar_width < pos[0] and event.button == 1: 
                        relatives_per_pixel = self.relatives_on_screen / self.display_height
                        relative_mouse_x = (event.pos[0] - self.sidebar_width) * relatives_per_pixel
                        relative_mouse_y = event.pos[1] * relatives_per_pixel
                        tile_x = int(self.relative_x//10 + relative_mouse_x // 10)
                        tile_y = int(self.relative_y//10 + relative_mouse_y // 10)
                        self._flood_fill(tile_x, tile_y, list(self.grid[tile_x, tile_y]), self.brush[0])

    def _grid_controller(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.relative_x_change = -1
                elif event.key == pygame.K_RIGHT:
                    self.relative_x_change = 1
                
                if event.key == pygame.K_DOWN:
                    self.relative_y_change = 1
            
                elif event.key == pygame.K_UP:
                    self.relative_y_change = -1

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
                pygame.draw.rect(gameDisplay, (int(color[0]), int(color[1]), int(color[2])), (x*10*pixels_per_relative - self.relative_x*pixels_per_relative, y*10*pixels_per_relative - self.relative_y*pixels_per_relative, pixels_per_relative*10, pixels_per_relative*10))

    def _draw_sidebar(self, gameDisplay):
        #slider 1
        pygame.draw.rect(gameDisplay, (0, 0, 0), (20, 20, self.sidebar_width-40, 20), 1)
        pygame.draw.rect(gameDisplay, (0, 0, 0), (20+self.slider_1_value, 20, 20, 20)) # implement color of hue
        
        #slider 2
        pygame.draw.rect(gameDisplay, (0, 0, 0), (20, 60, self.sidebar_width-40, 20), 1)
        pygame.draw.rect(gameDisplay, (0, 0, 0), (20+self.slider_2_value, 60, 20, 20))

        # water button
        text = self.myfont.render("Water: "+str(self.water), False, (0,0,0))
        gameDisplay.blit(text, (20, 100))

        text = self.myfont.render("Colorpicker: ", False, (0,0,0))
        text2 = self.myfont.render(str([ round(elem, 2) for elem in self.color_picker ]), False, (0,0,0))

        gameDisplay.blit(text, (20, 140))
        gameDisplay.blit(text2, (20, 165))
    
        text = self.myfont.render("Fill: "+str(self.fill), False, (0,0,0))
        gameDisplay.blit(text, (20, 200))
    
    def _flood_fill(self, x, y, old_color, new_color):
        if list(self.grid[x, y]) == old_color:
            self.grid[x,y] = new_color
            self._flood_fill(x, min(self.grid.shape[1]-1, y+1), old_color, new_color)
            self._flood_fill(x, max(0, y-1), old_color, new_color)
            self._flood_fill(min(self.grid.shape[0]-1, x+1), y, old_color, new_color)
            self._flood_fill(max(0, x-1), y, old_color, new_color)


gc = Game(800, 600,np.load("../grids/grid.npy"), 750)
while not gc.crashed:
    gc.next_frame()

np.save("grid.npy", gc.grid)