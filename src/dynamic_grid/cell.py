from __future__ import annotations

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

        self.particles = []

    def add(self, particle):
        self.particles.append(particle)

    def remove(self, obj):
        for particle in self.particles:
            if particle.object == obj:
                self.particles.remove(particle)
                return particle

    def to_up(self, particle):
        self.particles.remove(particle)
        self.up.add(particle)
        return self.up

    def to_right(self, particle):
        self.particles.remove(particle)
        self.right.add(particle)
        return self.right

    def to_down(self, particle: Particle):
        self.particles.remove(particle)
        self.down.add(particle)
        return self.down

    def to_left(self, particle: Particle):
        self.particles.remove(particle)
        self.left.add(particle)
        return self.left

    def __repr__(self):
        return f'n: {len(self.particles)}, ' + \
            f'({self.x1}, {self.y1}, {self.x2}, {self.y2})'
