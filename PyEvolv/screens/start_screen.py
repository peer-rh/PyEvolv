import pygame
from PyEvolv.assets.font import FONT
from PyEvolv.assets.icons import LOGO_PATH
import numpy as np

class StartingScreen:
    def __init__(self, height, width, bg_color, primary_color, secondary_color):
        self.height = height
        self.width = width

        self.bg_color = bg_color
        self.primary_color = primary_color
        self.secondary_color = secondary_color

        self.font = FONT
        self.surf: pygame.Surface = pygame.Surface((self.width, self.height))
        self._generate_background()
        self._generate_logo()
        self._generate_buttons()


    def next_frame(self):
        self.surf.fill(self.bg_color)
        self.surf.blit(self.background_surf, (0,0))
        self._draw_logo()
        self._draw_buttons()
    
    def starting_screen_controller(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.grid_creator_button.collidepoint(event.pos[0], event.pos[1]):
                self.grid_creator = True
            if self.game_button.collidepoint(event.pos[0], event.pos[1]):
                self.game = True

    def _draw_logo(self):
        self.surf.blit(self.logo_img, (self.logo_left, self.logo_top))
    
    def _generate_background(self):
        self.background_surf = pygame.Surface((self.width, self.height))
        background_tiles_y = int(self.height/ self.width * 10 + 1)
        grid_base = np.array([np.random.randint(100, 255), np.random.randint(100, 255), 0]) # to kepp contrast to logo
        grid = grid_base + np.random.randint(-20, 20, (10, background_tiles_y, 3))
        grid = np.maximum(0, np.minimum(255, grid))
        pixels_per_tile = self.width / 10
        for x in range(grid.shape[0]):
            for y in range(grid.shape[1]):
                color = grid[x, y]
                pygame.draw.rect(self.background_surf, color, (x*pixels_per_tile, y*pixels_per_tile, pixels_per_tile, pixels_per_tile))

    def _draw_buttons(self):
        pygame.draw.rect(self.surf, self.primary_color, self.grid_creator_button)
        pygame.draw.rect(self.surf, self.primary_color, self.game_button)

        self.surf.blit(self.grid_creator_text, self.grid_creator_text_dest)
        self.surf.blit(self.game_text, self.game_text_dest)

    def _generate_logo(self):
        self.logo_height, self.logo_width = 200, 588 # image is 1179 x 401, width is 1179/401*200
        self.logo_img = pygame.image.load(LOGO_PATH)
        self.logo_img = pygame.transform.scale(self.logo_img, (self.logo_width, self.logo_height))
        self.logo_top = 25
        self.logo_left = (self.width - self.logo_width) / 2

    def _generate_buttons(self):
        size_per_btn_w, size_per_btn_h =int(self.logo_width/1.5), 50
        current_y = 300

        self.grid_creator_button = pygame.Rect(int((self.width-size_per_btn_w)/2), current_y, size_per_btn_w, size_per_btn_h)
        self.grid_creator = False
        self.grid_creator_text = self.font.render("Grid Creator", False, self.bg_color)
        self.grid_creator_text_dest = (self.grid_creator_button.center[0] - self.grid_creator_text.get_rect().width/2, self.grid_creator_button.center[1] - self.grid_creator_text.get_rect().height/2)
        current_y += size_per_btn_h + 25

        self.game_button = pygame.Rect(int((self.width-size_per_btn_w)/2), current_y, size_per_btn_w, size_per_btn_h)
        self.game = False
        self.game_text = self.font.render("Game", False, self.bg_color)
        self.game_text_dest = (self.game_button.center[0] - self.game_text.get_rect().width/2, self.game_button.center[1] - self.game_text.get_rect().height/2)
        current_y += size_per_btn_h + 25