from __future__ import annotations
import pygame

class Cell:

    left: Cell
    right: Cell
    down: Cell
    up: Cell

    particles: List[Particle]

    # Bounding box
    x1: float
    y1: float
    x2: float
    y2: float

    max_particles = 2
    sub_divided = False
    divisions = []

    def __init__(self, x1, y1, x2, y2, up=None, right=None,
                 down=None, left=None):
        self.up = up
        self.right = right
        self.down = down
        self.left = left

        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

        self.n_particles = 0
        self.particles = []

    def add(self, particle):
        self.particles.append(particle)
        self.n_particles += 1

        if self.n_particles >= self.max_particles and not self.sub_divided:
            self.sub_divide()

    def sub_divide(self):
        # 1 2
        # 3 4

        self.sub_divided = True

        w = self.x2 - self.x1
        h = self.y2 - self.y1

        cell1 = Cell(self.x1, self.y1 + h/2, self.x1 + w/2, self.y2)
        cell2 = Cell(self.x1 + w/2, self.y1 + h/2, self.x1 + w, self.y2)
        cell3 = Cell(self.x1, self.y1, self.x1 + w/2, self.y1 + h/2)
        cell4 = Cell(self.x1 + w/2, self.y1, self.x1 + w, self.y1 + h/2)

        cell1.left = self.left
        cell1.right = cell2
        cell1.down = cell3
        cell1.up = self.up

        cell2.left = cell1
        cell2.down = cell4
        cell2.up = self.up
        cell2.right = self.right

        cell3.left = self.left
        cell3.down = self.down
        cell3.up = cell1
        cell3.right = cell4

        cell4.down = self.down
        cell4.right = self.right
        cell4.left = cell3
        cell4.up = cell2

        self.divisions = [[cell1, cell2], [cell3, cell4]]


    def undivide(self):

        self.divisions = []
        self.sub_divided = False

    def remove(self, obj):
        for particle in self.particles:
            if particle.object == obj:
                self.particles.remove(particle)
                return particle

    def rest_n_particles(self):
        self.n_particles -= 1

        if self.n_particles < self.max_particles:
            self.undivide()

    def to_up(self, particle):
        self.particles.remove(particle)
        self.rest_n_particles()
        self.up.add(particle)
        return self.up

    def to_right(self, particle):
        self.particles.remove(particle)
        self.rest_n_particles()
        self.right.add(particle)
        return self.right

    def to_down(self, particle: Particle):
        self.particles.remove(particle)
        self.rest_n_particles()
        self.down.add(particle)
        return self.down

    def to_left(self, particle: Particle):
        self.particles.remove(particle)
        self.rest_n_particles()
        self.left.add(particle)
        return self.left

    def draw(self, screen):
        if self.sub_divided:
            for row in self.divisions:
                for cell in row:
                    cell.draw(screen)

        x = self.x1
        y = self.y1
        w = self.x2 - x
        h = self.y2 - y

        n_particles = len(self.particles)
        if n_particles >= self.max_particles:
            color = (250, 100, 100)
        else:
            color = (100, 100, 100)

        pygame.draw.rect(screen, color, (x, y, w, h), 1)

    def __repr__(self):
        return f'n: {len(self.particles)}, ' + \
            f'({self.x1}, {self.y1}, {self.x2}, {self.y2})'
