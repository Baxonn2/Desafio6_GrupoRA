from src.dynamic_grid.cell import Cell
from typing import List
from src.dynamic_grid.particle import Particle
import pygame


class DynamicGrid:

    # Dimensiones del espacio
    SPACE_WIDTH = 600
    SPACE_HEIGHT = 600

    # Cantidad de casillas del espacio
    N_GRID_WIDTH = 6
    N_GRID_HEIGHT = 6

    # Malla
    __grid = List[List[Cell]]
    __particle_list = List[Particle]

    def __init__(self):

        cell_width = self.SPACE_WIDTH / self.N_GRID_WIDTH
        cell_height = self.SPACE_HEIGHT / self.N_GRID_HEIGHT

        self.__particle_list = []

        # Construyendo malla con celdas
        self.__grid = []
        for j in range(self.N_GRID_HEIGHT):
            self.__grid.append([])
            for i in range(self.N_GRID_WIDTH):
                x1 = i * cell_width
                y1 = j * cell_height
                x2 = x1 + cell_width
                y2 = y1 + cell_height
                self.__grid[j].append(Cell(x1, y1, x2, y2))

        # Uniendo las celdas
        for j, cell_row in enumerate(self.__grid):
            for i, cell in enumerate(cell_row):
                if j > 0:
                    cell.up = self.__grid[j - 1][i]
                if i > 0:
                    cell.left = self.__grid[j][i - 1]
                if j < self.N_GRID_HEIGHT - 1:
                    cell.down = self.__grid[j + 1][i]
                if i < self.N_GRID_WIDTH - 1:
                    cell.right = self.__grid[j][i + 1]

    def get_cell(self, i, j):
        return self.__grid[j][i]

    def update(self):
        for particle in self.__particle_list:
            particle.update()

    def add(self, x, y, obj):
        i = int(x / self.SPACE_WIDTH * self.N_GRID_WIDTH)
        j = int(y / self.SPACE_HEIGHT * self.N_GRID_HEIGHT)

        cell = self.__grid[j][i]
        particle = Particle(obj, cell, x, y)
        cell.add(particle)

        self.__particle_list.append(particle)

        return particle

    def remove(self, x, y, obj):
        i = int(x / self.SPACE_WIDTH * self.N_GRID_WIDTH)
        j = int(y / self.SPACE_HEIGHT * self.N_GRID_HEIGHT)

        cell = self.__grid[j][i]
        particle = cell.remove(obj)
        self.__particle_list.remove(particle)

    def draw(self, screen, color):
        for cell_row in self.__grid:
            for cell in cell_row:
                x = cell.x1
                y = cell.y1
                w = cell.x2 - x
                h = cell.y2 - y
                pygame.draw.rect(screen, color, (x, y, w, h), 1)

    def get(self, x, y, param):
        # TODO: programar esta funcion
        i = int(x / self.SPACE_WIDTH * self.N_GRID_WIDTH)
        j = int(y / self.SPACE_HEIGHT * self.N_GRID_HEIGHT)

        cell = self.__grid[j][i]

        result = []
        for particle in cell.particles:
            result.append(particle.object)

        return result