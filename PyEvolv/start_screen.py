import pygame
from PyEvolv.assets.font import FONT

class StartingScreen:
    def __init__(self, height, width, bg_color, primary_color, secondary_color):
        self.height = height
        self.width = width

        self.bg_color = bg_color
        self.primary_color = primary_color
        self.secondary_color = secondary_color

        self.font = FONT
        self.surf = pygame.Surface((self.width, self.height))
        self._generate_buttons()


    def next_frame(self):
        self.surf.fill(self.bg_color)
        self._draw_buttons()
    
    def starting_screen_controller(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.grid_creator_button.collidepoint(event.pos[0], event.pos[1]):
                self.grid_creator = True
            if self.game_button.collidepoint(event.pos[0], event.pos[1]):
                self.game = True

    def _draw_buttons(self):
        pygame.draw.rect(self.surf, self.primary_color, self.grid_creator_button)
        pygame.draw.rect(self.surf, self.primary_color, self.game_button)

        self.surf.blit(self.grid_creator_text, self.grid_creator_text_dest)
        self.surf.blit(self.game_text, self.game_text_dest)

    def _generate_buttons(self):
        size_per_btn_w, size_per_btn_h = (int(self.width-150)/2), self.height-100
        self.grid_creator_button = pygame.Rect(50, 50, size_per_btn_w, size_per_btn_h)
        self.grid_creator = False
        self.grid_creator_text = self.font.render("Grid Creator", False, self.bg_color)
        self.grid_creator_text_dest = (self.grid_creator_button.center[0] - self.grid_creator_text.get_rect().width/2, self.grid_creator_button.center[1] - self.grid_creator_text.get_rect().height/2)

        self.game_button = pygame.Rect(size_per_btn_w+100, 50, size_per_btn_w, size_per_btn_h)
        self.game = False
        self.game_text = self.font.render("Game", False, self.bg_color)
        self.game_text_dest = (self.game_button.center[0] - self.game_text.get_rect().width/2, self.game_button.center[1] - self.game_text.get_rect().height/2)

def main():
    pygame.init()

    sc = StartingScreen(600, 800, (255,255,255), (0,0,0), (0,0,255))
    gD = pygame.display.set_mode((800, 600))
    while True:
        events = pygame.event.get()
        for event in events:
            sc.starting_screen_controller(event)

        sc.next_frame()
        gD.blit(sc.surf, (0,0))
        pygame.display.update()
