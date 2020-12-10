#import dynamic_grid as dg
from src.dynamic_grid.dynamic_grid import DynamicGrid
from src.entity import Entity
from random import random


def main():
    grid = DynamicGrid()
    entity_list = []

    for i in range(100):
        x = 200  # random() * 400
        y = 200  # random() * 400
        entity = Entity(x, y)
        particle = grid.add(x, y, entity)
        entity_list.append(particle)

    entity_list[0].object.set_target_position(300, 350)

    for i in range(100):
        entity_list[0].update()


if __name__ == "__main__":
    main()
