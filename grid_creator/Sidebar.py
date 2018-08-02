import pygame
import colorsys
import numpy as np
import cv2

class Sidebar:
    def __init__(self, width, height, background_color=(255, 255, 255), primary_color=(0,0,0), primary_color_2=(0,0,255)):
        self.width = width
        self.height = height
        self.background_color = background_color
        self.primary_color = primary_color
        self.primary_color_2 = primary_color_2
        
        self.sidebar_surf = pygame.Surface((width, height))

        self.slider_1_val = 0
        self.slider_1_rgb = colorsys.hsv_to_rgb(self.slider_1_val/(width-40), 1, 1)
        self.slider_2_val = 0
        self.slider_2_rgb = colorsys.hsv_to_rgb(self.slider_1_val/(width-40), self.slider_2_val/(width-40), 1)

        self.place_between_tools = (width - 40 - 3 * 32) // 2

        self.water = False
        self._generate_water_img()

        self.color_picker = False
        self._generate_color_picker_img()
    
        self.fill = False
        self._generate_fill_img()
    
    def next_frame(self, events):
        self._sidebar_controller(events)
        self._draw_slider_1()
        self._draw_slider_2()
        self._draw_tools()
    
    def _sidebar_controller(self, events):
        for event in events:
            if event.type == pygame.MOUSEMOTION:
                if 20 <= event.pos[0] <= self.width - 40 and 20 < event.pos[1] < 40 and event.buttons[0] == 1:
                    self.slider_1_val = event.pos[0] - 20
                    self.slider_1_rgb = colorsys.hsv_to_rgb(self.slider_1_val/(self.width-40), 1, 1)

                if 20 <= event.pos[0] <= self.width - 40 and 60 < event.pos[1] < 80 and event.buttons[0] == 1:
                    self.slider_2_val = event.pos[0] - 20
                    self.slider_2_rgb = colorsys.hsv_to_rgb(self.slider_1_val/(self.width-40), self.slider_2_val/(self.width-40), 1)

    def _draw_slider_1(self):
        pygame.draw.rect(self.sidebar_surf, self.primary_color, (20, 20, self.width-40, 20), 1)
        pygame.draw.rect(self.sidebar_surf, self.slider_1_rgb, (20+self.slider_1_val, 20, 20, 20))

    def _draw_slider_2(self):
        pygame.draw.rect(self.sidebar_surf, self.primary_color, (20, 60, self.width-40, 20), 1)
        pygame.draw.rect(self.sidebar_surf, self.slider_2_rgb, (20+self.slider_2_val, 60, 20, 20))
    
    def _draw_tools(self):
        if self.water:
            self.sidebar_surf.blit(self.water_img_on, (20, 100))
        else:
            self.sidebar_surf.blit(self.water_img_off, (20, 100))

        if self.color_picker:
            self.sidebar_surf.blit(self.color_picker_img_on, (52+self.place_between_tools, 100))
        else:
            self.sidebar_surf.blit(self.color_picker_img_off, (52+self.place_between_tools, 100))

        if self.fill:
            self.sidebar_surf.blit(self.fill_img_on, (84+2*self.place_between_tools, 100))
        else:
            self.sidebar_surf.blit(self.fill_img_off, (84+2*self.place_between_tools, 100))
    
    def _generate_water_img(self):
        img = cv2.imread("assets/water.png", 1)
        img = cv2.resize(img, (32, 32))
        self.water_img_off = (np.abs(img-255)/255) * self.primary_color
        self.water_img_on = (np.abs(img-255)/255) * self.primary_color_2
        self.water_img_off = pygame.pixelcopy.make_surface(self.water_img_off.astype("int"))
        self.water_img_on = pygame.pixelcopy.make_surface(self.water_img_on.astype("int"))
    
    def _generate_color_picker_img(self):
        img = cv2.imread("assets/color_picker.png", 1)
        img = cv2.resize(img, (32, 32))
        self.color_picker_img_off = (np.abs(img-255)/255) * self.primary_color
        self.color_picker_img_on = (np.abs(img-255)/255) * self.primary_color_2
        self.color_picker_img_off = pygame.pixelcopy.make_surface(self.color_picker_img_off.astype("int"))
        self.color_picker_img_on = pygame.pixelcopy.make_surface(self.color_picker_img_on.astype("int"))
    
    def _generate_fill_img(self):
        img = cv2.imread("assets/fill_bucket.png", 1)
        img = cv2.resize(img, (32, 32))
        self.fill_img_off = (np.abs(img-255)/255) * self.primary_color
        self.fill_img_on = (np.abs(img-255)/255) * self.primary_color_2
        self.fill_img_off = pygame.pixelcopy.make_surface(self.fill_img_off.astype("int"))
        self.fill_img_on = pygame.pixelcopy.make_surface(self.fill_img_on.astype("int"))

if __name__ == "__main__":
    pygame.init()
    gameDisplay = pygame.display.set_mode((200,600))
    pygame.display.set_caption('Sidebar')
    sd = Sidebar(200, 600)
    while True:
        sd.next_frame(pygame.event.get())
        gameDisplay.blit(sd.sidebar_surf, (0,0))