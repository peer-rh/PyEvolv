import pygame
import colorsys
import numpy as np
import cv2
from scipy import ndimage


class Sidebar:
    def __init__(self, width, height, background_color=(255, 255, 255), primary_color=(0,0,0), primary_color_2=(0,0,255)):
        """The Sidebar of the grid_creator
        
        Arguments:
            width {int} -- The width in pixels of the sidebar
            height {int} -- The height in pixels of the sidebar
        
        Keyword Arguments:
            background_color {tuple} -- The background color of the Sidebar (default: {(255, 255, 255)})
            primary_color {tuple} -- The primary color of the sidebar (default: {(0,0,0)})
            primary_color_2 {tuple} -- The second primary color of the sidebar (default: {(0,0,255)})
        """

        self.width = width
        self.height = height
        self.background_color = background_color
        self.primary_color = primary_color
        self.primary_color_2 = primary_color_2
        
        self.sidebar_surf = pygame.Surface((width, height))
        self.font = pygame.font.Font('../Arial.ttf', 20)

        self.update_slider(0,0)

        self.place_between_tools = (width - 40 - 3 * 32) // 2

        self.water = False
        self._generate_water_img()

        self.color_picker = False
        self._generate_color_picker_img()
    
        self.fill = False
        self._generate_fill_img()

        self._make_save_load()
        
    def next_frame(self):
        """The next fame on the sidebar surface. It draws and displays everything
        """

        self.sidebar_surf.fill(self.background_color)
        self._draw_slider_1()
        self._draw_slider_2()
        self._draw_tools()
        self._draw_save_load()
    
    def update_slider(self, slider_1_val, slider_2_val):
        """Function to update slider_vals
        
        Arguments:
            slider_1_val {int} -- The slider 1 value in pixels from the starting point
            slider_2_val {int} -- The slider 2 value in pixels from the starting point
        """

        self.slider_1_val = slider_1_val
        self.slider_1_rgb = np.asarray(colorsys.hsv_to_rgb(self.slider_1_val/(self.width-60), 1, 1)) * 255
        self.slider_2_val = slider_2_val
        self.slider_2_rgb = np.asarray(colorsys.hsv_to_rgb(self.slider_1_val/(self.width-60), self.slider_2_val/(self.width-40), 1)) * 255

    def controller(self, event):
        """The controller for the Sidebar
        
        Arguments:
            event {event} -- One single event from pygame.event.get
        """ 

        if not self.text_field_selected:
            if event.type == pygame.MOUSEMOTION:
                if 20 <= event.pos[0] <= self.width - 40 and 20 < event.pos[1] < 40 and event.buttons[0] == 1:
                    self.update_slider(event.pos[0]-20, self.slider_2_val)

                elif 20 <= event.pos[0] <= self.width - 40 and 60 < event.pos[1] < 80 and event.buttons[0] == 1:
                    self.update_slider(self.slider_1_val, event.pos[0]-20)


            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if 100 <= mouse_pos[1] <= 132:
                    if 0 <= mouse_pos[0] - 20 <= 32:

                        self.water = np.abs(self.water-1)
                        self.color_picker = 0
                        self.fill = 0

                    elif 0 <= mouse_pos[0] - (52+self.place_between_tools) <= 32:
                        self.water = 0
                        self.color_picker = np.abs(self.color_picker-1)
                        self.fill = 0

                    elif 0 <= mouse_pos[0] - (84+2*self.place_between_tools) <= 32:
                        self.water = 0
                        self.color_picker = 0
                        self.fill = np.abs(self.fill-1)
                
                if self.text_field.collidepoint(event.pos[0], event.pos[1]):
                    self.text_field_selected = True
                
                if self.save_button.collidepoint(event.pos[0], event.pos[1]):
                    self.save = True

                if self.load_button.collidepoint(event.pos[0], event.pos[1]):
                    self.load = True
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.grid_name = self.grid_name[:-1]
                    self.grid_name_surf = self.font.render(self.grid_name, True, self.primary_color)
                elif event.key == pygame.K_RETURN:
                    self.text_field_selected = False
                elif event.unicode in self.possible_name_keys:
                    self.grid_name += event.unicode
                    self.grid_name_surf = self.font.render(self.grid_name, True, self.primary_color)

    def _draw_slider_1(self):
        """draw slider 1
        """

        pygame.draw.rect(self.sidebar_surf, self.primary_color, (20, 20, self.width-40, 20), 1)
        pygame.draw.rect(self.sidebar_surf, self.slider_1_rgb, (20+self.slider_1_val, 20, 20, 20))

    def _draw_slider_2(self):
        """draw slider 2
        """

        pygame.draw.rect(self.sidebar_surf, self.primary_color, (20, 60, self.width-40, 20), 1)
        pygame.draw.rect(self.sidebar_surf, self.slider_2_rgb, (20+self.slider_2_val, 60, 20, 20))
    
    def _draw_tools(self):
        """draw all the 3 tools, water, color picker and fill
        """

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
    
    def _draw_save_load(self):
        """draw the save and load section
        """

        pygame.draw.rect(self.sidebar_surf, self.primary_color, self.text_field, 2)
        self.sidebar_surf.blit(self.grid_name_surf, (25, self.height - 125))

        pygame.draw.rect(self.sidebar_surf, self.primary_color, self.save_button)
        pygame.draw.rect(self.sidebar_surf, self.primary_color, self.load_button)
        self.sidebar_surf.blit(self.save_text, self.save_text_dest)
        self.sidebar_surf.blit(self.load_text, self.load_text_dest)
    
    def _generate_water_img(self):
        """generate the water icon based on the primary colors
        """

        img = cv2.imread("assets/water.png", cv2.IMREAD_UNCHANGED)
        img = cv2.resize(img, (32, 32))

        indexes = np.where(img[:,:,3] == 0)
        indexes_2 = np.where(img[:,:,3] != 0)
        img = img[:,:,:3]
        img[indexes[0], indexes[1]] = self.background_color

        self.water_img_off = np.copy(img)
        self.water_img_off[indexes_2[0], indexes_2[1]] = self.primary_color
        self.water_img_on = np.copy(img)
        self.water_img_on[indexes_2[0], indexes_2[1]] = self.primary_color_2

        self.water_img_off = pygame.pixelcopy.make_surface(self.water_img_off.astype("int"))
        center = self.water_img_off.get_rect().center
        self.water_img_off = pygame.transform.rotate(self.water_img_off, -90)
        self.water_img_off.get_rect().center = center

        self.water_img_on = pygame.pixelcopy.make_surface(self.water_img_on.astype("int"))
        self.water_img_on = pygame.transform.rotate(self.water_img_on, -90)
        self.water_img_on.get_rect().center = center

    def _generate_color_picker_img(self):
        """generate the color picker icon based on the primary colors
        """

        img = cv2.imread("assets/color_picker.png", cv2.IMREAD_UNCHANGED)
        img = cv2.resize(img, (32, 32))
        indexes = np.where(img[:,:,3] == 0)
        indexes_2 = np.where(img[:,:,3] != 0)
        img = img[:,:,:3]
        img[indexes[0], indexes[1]] = self.background_color

        self.color_picker_img_off = np.copy(img)
        self.color_picker_img_off[indexes_2[0], indexes_2[1]] = self.primary_color
        self.color_picker_img_on = np.copy(img)
        self.color_picker_img_on[indexes_2[0], indexes_2[1]] = self.primary_color_2

        self.color_picker_img_off = pygame.pixelcopy.make_surface(self.color_picker_img_off.astype("int"))
        self.color_picker_img_on = pygame.pixelcopy.make_surface(self.color_picker_img_on.astype("int"))

    
    def _generate_fill_img(self):
        """generate the fill bucket icon based on the primary colors
        """

        img = cv2.imread("assets/fill_bucket.png", cv2.IMREAD_UNCHANGED)
        img = cv2.resize(img, (32, 32))
        indexes = np.where(img[:,:,3] == 0)
        indexes_2 = np.where(img[:,:,3] != 0)
        img = img[:,:,:3]
        img[indexes[0], indexes[1]] = self.background_color

        self.fill_img_off = np.copy(img)
        self.fill_img_off[indexes_2[0], indexes_2[1]] = self.primary_color
        self.fill_img_on = np.copy(img)
        self.fill_img_on[indexes_2[0], indexes_2[1]] = self.primary_color_2

        self.fill_img_off = pygame.pixelcopy.make_surface(self.fill_img_off.astype("int"))
        center = self.fill_img_off.get_rect().center
        self.fill_img_off = pygame.transform.rotate(self.fill_img_off, -90)
        self.fill_img_off.get_rect().center = center
        self.fill_img_off = pygame.transform.flip(self.fill_img_off, True, False)


        self.fill_img_on = pygame.pixelcopy.make_surface(self.fill_img_on.astype("int"))
        self.fill_img_on = pygame.transform.rotate(self.fill_img_on, -90)
        self.fill_img_on.get_rect().center = center
        self.fill_img_on = pygame.transform.flip(self.fill_img_on, True, False)
        
    def _make_save_load(self):
        """generate the text and rects for the save and load section
        """

        self.text_field = pygame.Rect(20, self.height-140, self.width-40, 50)
        self.grid_name = "grid"
        self.grid_name_surf = self.font.render(self.grid_name, True, self.primary_color)
        self.possible_name_keys = ".abcdefghijklmnopqrstuvwxyz1234567890_"
        self.text_field_selected = False

        self.button_size = (self.width - 60) / 2
        self.save_button = pygame.Rect(20, self.height - 70, self.button_size, 50)
        self.save_text = self.font.render("Save", False, self.background_color)
        self.save_text_dest = (self.save_button.center[0] - self.save_text.get_rect().width/2, self.save_button.center[1] - self.save_text.get_rect().height/2)
        self.save = False

        self.load_button = pygame.Rect(40+self.button_size, self.height - 70, self.button_size, 50)
        self.load_text = self.font.render("Load", False, self.background_color)
        self.load_text_dest = (self.load_button.center[0] - self.load_text.get_rect().width/2, self.load_button.center[1] - self.load_text.get_rect().height/2)
        self.load = False 