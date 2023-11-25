import sys
import pygame
import numpy as np

from copy import deepcopy
from numba import njit
from random import randint


class Automaton:
    def __init__(self, 
                 window_size: tuple, pixel_size: int, fps: int,
                 random_fill: bool = True, barrier_percent: int = 0,
                 **settings) -> None:
        
        pygame.init()
        pygame.display.set_caption("Game of Life - AdamantiumCode")
        pygame.display.set_icon(pygame.Surface([30,30], pygame.SRCALPHA, 32))

        self.pixel = pixel_size
        self.fps = fps
        
        self.barrier_percent = barrier_percent
        self.random_fill = random_fill
        
        if settings:
            if settings.get("V"):
                if settings["V"] == "8":
                    self.view == "all"
                elif settings["V"] == "4c":
                    self.view = "cross"
                elif settings["V"] == "4d":
                    self.view = "diagonal"
                else:
                    print("Wrong value on V parametr!")
            else:
                self.view = "all"
            
            if settings.get("B"):
                self.can_born = np.array(settings["B"])
            else:
                self.can_born = np.array([3])
            
            if settings.get("S"):
                self.can_survive = np.array(settings["S"])
            else:
                self.can_survive = np.array([2, 3])
        
        else:
            self.view = "all"
            self.can_survive = np.array([2, 3])
            self.can_born = np.array([3])
            
        self.width = window_size[0] // self.pixel
        self.height = window_size[1] // self.pixel
        
        self.surface = pygame.display.set_mode(window_size)
        self.clock = pygame.time.Clock()
        
        self.next_cells = self.clear_cells()
        
        if self.random_fill:
            self.current_cells = self.random_spawn_cells()
        else:
            self.current_cells = self.spawn_rect_cells()
        
    def reset(self):
        if self.random_fill:
            self.current_cells = self.random_spawn_cells()
        else:
            self.current_cells = self.spawn_rect_cells()
    
    def clear_cells(self) -> np.ndarray:
        return np.array(
            [[0 for _ in range(self.width)] 
             for _ in range(self.height)]
        )
    
    def random_spawn_cells(self) -> np.ndarray:
        barr_w = self.width * self.barrier_percent // 200
        barr_h = self.height * self.barrier_percent // 200
        return np.array(
            [[randint(0, 1) if barr_w <= i <= self.width - barr_w and barr_h <= j <= self.height - barr_h
            else 0
            for i in range(self.width)]
            for j in range(self.height)]
            )
    
    def spawn_rect_cells(self) -> np.ndarray:
        barr_w = self.width * self.barrier_percent // 200
        barr_h = self.height * self.barrier_percent // 200
        return np.array(
            [[1 if barr_w <= i <= self.width - barr_w and barr_h <= j <= self.height - barr_h
            else 0
            for i in range(self.width)]
            for j in range(self.height)]
            )
    
    def spawn_cell(self, positions: tuple) -> None:
        x = positions[0] // self.pixel
        y = positions[1] // self.pixel
        
        if (0 >= x or x >= self.width - 1 or 0 >= y or y >= self.height - 1):
            return
        
        self.current_cells[y][x] = 1
        self.next_cells[y][x] = 1
        pygame.draw.rect(self.surface, pygame.Color('darkgreen'),
                          (x * self.pixel + 1, 
                           y * self.pixel + 1, 
                           self.pixel - 1, 
                           self.pixel - 1))
        
        pygame.display.flip()
            
    @staticmethod
    @njit(fastmath=True)
    def check_all_cells(current_cells: list, next_cells: list,
                    can_survive, can_born,
                    width: int, height: int) -> tuple:
        result = []
        for x in range(1, width - 1):
            for y in range(1, height - 1):
                count = 0
                for j in range(y - 1, y + 2):
                    for i in range(x - 1, x + 2):
                        if current_cells[j][i]:
                            count += 1
                
                if current_cells[y][x]:
                    count -= 1

                    if count in can_survive:
                        next_cells[y][x] = 1
                        result.append((x, y))
                    else:
                        next_cells[y][x] = 0
                else:
                    if count in can_born:
                        next_cells[y][x] = 1
                        result.append((x, y))
                    else:
                        next_cells[y][x] = 0
        return next_cells, result
    
    @staticmethod
    @njit(fastmath=True)
    def check_diagonal_cells(current_cells: list, next_cells: list,
                    can_survive, can_born,
                    width: int, height: int) -> tuple:
        result = []
        for x in range(1, width - 1):
            for y in range(1, height - 1):
                count = 0
                
                for j in range(y + 1, y - 2, -2):
                    for i in range(x - 1, x + 2, 2):
                        if current_cells[j][i]:
                            count += 1
                
                if current_cells[y][x]:
                    if count in can_survive:
                        next_cells[y][x] = 1
                        result.append((x, y))
                    else:
                        next_cells[y][x] = 0
                        
                else:
                    if count in can_born:
                        next_cells[y][x] = 1
                        result.append((x, y))
                    else:
                        next_cells[y][x] = 0
                        
        return next_cells, result
    
    @staticmethod
    @njit(fastmath=True)
    def check_cross_cells(current_cells: list, next_cells: list,
                    can_survive, can_born,
                    width: int, height: int) -> tuple:
        result = []
        for x in range(1, width - 1):
            for y in range(1, height - 1):
                count = 0
                
                if current_cells[y+1][x]:
                    count += 1
                if current_cells[y][x-1]:
                    count += 1
                if current_cells[y][x+1]:
                    count += 1
                if current_cells[y-1][x]:
                    count += 1
                
                if current_cells[y][x]:
                    if count in can_survive:
                        next_cells[y][x] = 1
                        result.append((x, y))
                    else:
                        next_cells[y][x] = 0
                        
                else:
                    if count in can_born:
                        next_cells[y][x] = 1
                        result.append((x, y))
                    else:
                        next_cells[y][x] = 0
                        
        return next_cells, result

    def draw(self) -> None:
        self.surface.fill(pygame.Color('black'))
        
        if self.view == "all":
            self.next_cells, result = self.check_all_cells(
                self.current_cells, 
                self.next_cells,
                self.can_survive,
                self.can_born,
                self.width, 
                self.height,
                )
        
        elif self.view == "diagonal":
            self.next_cells, result = self.check_diagonal_cells(
                self.current_cells, 
                self.next_cells,
                self.can_survive,
                self.can_born,
                self.width, 
                self.height,
                )
        
        else:
            self.next_cells, result = self.check_cross_cells(
                self.current_cells, 
                self.next_cells,
                self.can_survive,
                self.can_born,
                self.width, 
                self.height,
                )
        
        [pygame.draw.rect(self.surface, pygame.Color('darkgreen'),
                          (x * self.pixel + 1, 
                           y * self.pixel + 1, 
                           self.pixel - 1, 
                           self.pixel - 1))
         for x, y in result]
        
        self.current_cells = deepcopy(self.next_cells)
        
        pygame.display.flip()
        self.clock.tick(self.fps)


if __name__ == "__main__":
    automaton = Automaton(
        window_size=(1400, 700), 
        pixel_size=20, 
        fps=20,
        random_fill=True,
        barrier_percent=10,
        )
    
    pause = False
    click = False
    
    while True:
        if not(pause):
            automaton.draw()
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                sys.exit()
            elif (event.type == pygame.KEYDOWN):
                if (event.key == pygame.K_p):
                    pause = not pause
                elif (event.key == pygame.K_MINUS):
                    automaton.fps -= 2
                elif (event.key == pygame.K_EQUALS):
                    automaton.fps += 2
                elif (event.key == pygame.K_c):
                    automaton.current_cells = automaton.clear_cells()
                elif (event.key == pygame.K_r):
                    automaton.reset()
                elif (event.key == pygame.K_f):
                    automaton.current_cells = automaton.spawn_rect_cells()
                elif (event.key == pygame.K_m):
                    automaton.fps = -1
            
            elif (event.type == pygame.MOUSEBUTTONDOWN):
                click = True
                automaton.spawn_cell(event.pos)
            
            elif (event.type == pygame.MOUSEBUTTONUP):
                click = False
            
            elif (event.type == pygame.MOUSEMOTION and click):
                automaton.spawn_cell(event.pos)
