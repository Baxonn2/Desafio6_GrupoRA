from typing import List
from random import random

class Particle:

    # Posicion actual
    x: float
    y: float

    # Posicion objetivo
    _x_target: float
    _y_target: float

    # Donde se encuentra la particula
    dg: DynamicGrid

    TARGET_DONE_RANGE = 0.5

    def __init__(self, x: float, y: float, dg: DynamicGrid):
        self.x = x
        self.y = y
        self._x_target = x
        self._y_target = y
        self.dg = dg

    def update(self):
        dx = (self._x_target - self.x) / 20
        dy = (self._y_target - self.y) / 20

        MAX = 1

        if abs(dx) > MAX:
            dx = MAX if dx > 0 else -MAX
        if abs(dy) > MAX:
            dy = MAX if dy > 0 else -MAX

        self.x += dx
        self.y += dy

        target_done = abs(dx) < self.TARGET_DONE_RANGE and \
            abs(dy) < self.TARGET_DONE_RANGE

        if target_done:
            self._x_target = random() * 400
            self._y_target = random() * 400

    def notify(self, x, y, x2, y2):
        # Llama a la función update del DynamicGrid para cambiar de casilla a
        # la particula
        self.dg.add_to_update(self, x, y, x2, y2)


class DynamicGrid:

    # Maximo de particulas en una casilla
    MAX_GRID_PARTICLES = 10

    # Dimensiones del espacio
    SPACE_WIDTH = 400
    SPACE_HEIGHT = 400

    # Cantidad de casillas del espacio
    N_GRID_WIDTH = 5
    N_GRID_HEIGHT = 4

    # Contenedores
    __grid = List[List[Particle]]
    __all_particles = List[Particle]

    def __init__(self):

        # Inicializando grid
        self.__grid = []
        for _ in range(self.N_GRID_HEIGHT):
            self.__grid.append([[]] * self.N_GRID_WIDTH)

        # Incializando lista de todas las particulas
        self.__all_particles = []

    def add(self, particle: Particle):
        x = int(particle.x / self.SPACE_WIDTH * self.N_GRID_WIDTH)
        y = int(particle.y / self.SPACE_HEIGHT * self.N_GRID_HEIGHT)

        print(x, y)
        self.__grid[y][x].append(particle)
        self.__all_particles.append(particle)

        # Si la lista __grid[y][x] supera el maximo se tiene que dividir
        if len(self.__grid[y][x]) > self.MAX_GRID_PARTICLES:
            print("Necesario crear nuevo grid")

    def update(self):
        for particle in self.__all_particles:
            particle.update()

    def add_to_update(self, particle: Particle, x, y, x2, y2):
