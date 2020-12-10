from src.dynamic_grid.cell import Cell

class Particle:

    def __init__(self, obj, cell: Cell, x: float, y: float):
        self.x = x
        self.y = y
        self.cell = cell
        self.object = obj

    def update(self):

        # print(f"actual position: {self.x, self.y} , Cell: {self.cell}")

        # Aqui falta el update
        self.x, self.y = self.object.x, self.object.y

        # print(f"new position: {self.x, self.y} , Cell: {self.cell}")

        # Actualizando celda
        if self.x > self.cell.x2:
            self.cell = self.cell.to_right(self)
        elif self.x < self.cell.x1:
            self.cell = self.cell.to_left(self)

        if self.y > self.cell.y2:
            self.cell = self.cell.to_down(self)
        elif self.y < self.cell.y1:
            self.cell = self.cell.to_up(self)
