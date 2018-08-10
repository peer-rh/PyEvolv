            self.gameDisplay.blit(self.starting_screen.surf, (0,0))
        
        elif self.current_env == "game":
            self.gameDisplay.fill((255, 0, 0))
            pygame.draw.rect(self.gameDisplay, self.bg_color, (0,0,self.width, 50))
            self.gameDisplay.blit(self.back_txt, (15, 15))
 
            if self.game == None:
                self._generate_game()
            for _ in range(self.constants["evo_steps_per_frame"]):
                self.evolution.next_step()
            
            self.game.update_grid(self.evolution.grid)
            self.game.next_frame(self.evolution.creatures, self.evolution.creatures_per_species_count)
            self.gameDisplay.blit(self.game.surf, (0, 50))
 
        elif self.current_env == "grid_creator":
            self.gameDisplay.fill((0, 255, 0))
            pygame.draw.rect(self.gameDisplay, self.bg_color, (0,0,self.width, 50))
            self.gameDisplay.blit(self.back_txt, (15, 15))
            if self.grid_creator == None:
                self._generate_grid_creator()
            self.grid_creator.next_frame()
            self.gameDisplay.blit(self.grid_creator.surf, (0, 50))
            
    def _controller(self, event:pygame.event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.current_env != "start_screen" and 0 < event.pos[0] < self.back_txt.get_rect().width + 15 and 0 < event.pos[1] < 50:
                self.current_env = "start_screen"
                self.grid_creator = None
                self.game = None
                self.evolution = None
    
    def _starting_screen_bridge(self) -> None:
        if self.starting_screen.game:
            self.current_env = "game"
            self.starting_screen.game = False
        
        elif self.starting_screen.grid_creator:
            self.current_env = "grid_creator"
            self.starting_screen.grid_creator = False
    
    def _generate_game(self) -> None:
        grid = np.load(self.grids_path + "/grid.npy")
        self.evolution = Evolution(self.constants["n_population"], grid, self.constants)
        self.game = Game(self.width, self.height-50, 50, grid, 750, self.constants)
    
    def _generate_grid_creator(self) -> None:
        self.grid_creator = GridCreator(self.width, self.height-50, np.zeros((75, 75, 3)), self.grids_path+"/", 750, 50, self.bg_color, self.primary_color, self.secondary_color)