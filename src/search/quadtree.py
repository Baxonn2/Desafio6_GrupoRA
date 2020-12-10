import math
import pygame


class Node:
    NODE_ID = 1
    max_w = 0
    max_h = 0

    def __init__(self, x, y, w, h, capacity, parent=None):
        if parent is None:
            Node.NODE_ID = 1
            Node.max_w = w
            Node.max_h = h
        else:
            Node.NODE_ID += 1
        self.n_id = Node.NODE_ID
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.capacity = capacity
        self.entities = []
        self.divided = False
        self.parent = parent
        self.upper_right_child = None
        self.upper_left_child = None
        self.down_right_child = None
        self.down_left_child = None

    def contains(self, x, y):
        return self.x + self.w > x >= self.x - self.w and \
               self.y + self.h > y >= self.y - self.h

    def subdivide(self):
        self.upper_right_child = Node(self.x + self.w / 2, self.y - self.h / 2,
                                      self.w / 2, self.h / 2, self.capacity, self)
        self.upper_left_child = Node(self.x - self.w / 2, self.y - self.h / 2,
                                     self.w / 2, self.h / 2, self.capacity, self)
        self.down_right_child = Node(self.x + self.w / 2, self.y + self.h / 2,
                                     self.w / 2, self.h / 2, self.capacity, self)
        self.down_left_child = Node(self.x - self.w / 2, self.y + self.h / 2,
                                    self.w / 2, self.h / 2, self.capacity, self)
        self.divided = True

        for entity in self.entities:
            self.upper_left_child.insert(entity)
            self.upper_right_child.insert(entity)
            self.down_left_child.insert(entity)
            self.down_right_child.insert(entity)

        self.entities = []

    def insert(self, entity):
        if not self.contains(entity.x, entity.y):
            return False
        if len(self.entities) <= self.capacity and not self.divided:
            self.entities.append(entity)
        else:
            if not self.divided:
                self.subdivide()
            self.upper_left_child.insert(entity)
            self.upper_right_child.insert(entity)
            self.down_left_child.insert(entity)
            self.down_right_child.insert(entity)

    def find_neighbors(self, x, y, radius):
        points = []

        if x+radius < Node.max_w:
            points.append((x+radius, y))
        if x-radius > 0:
            points.append((x - radius, y))
        if y+radius < Node.max_h:
            points.append((x, y + radius))
        if y-radius > 0:
            points.append((x, y - radius))

        is_parent = False

        base_node = self.find_node(x, y)
        contains_all = False

        while not contains_all:
            if base_node.parent is None:
                break
            contains_all = True
            for _ in points:
                x_, y_ = _[0], _[1]
                if not base_node.contains(x_, y_):
                    contains_all = False
                    base_node = base_node.parent
                    is_parent = True

        entities = []

        if is_parent:
            upper_right = False
            down_right = False
            upper_left = False
            down_left = False
            if (base_node.upper_right_child.contains(x+radius, y) or
                base_node.upper_right_child.contains(x - radius, y) or
                base_node.upper_right_child.contains(x, y + radius) or
                base_node.upper_right_child.contains(x, y - radius)
                ):
                upper_right = True
            if (base_node.upper_left_child.contains(x + radius, y) or
                    base_node.upper_left_child.contains(x - radius, y) or
                    base_node.upper_left_child.contains(x, y + radius) or
                    base_node.upper_left_child.contains(x, y - radius)
            ):
                upper_left = True
            if (base_node.down_right_child.contains(x+radius, y) or
                base_node.down_right_child.contains(x - radius, y) or
                base_node.down_right_child.contains(x, y + radius) or
                base_node.down_right_child.contains(x, y - radius)
                ):
                down_right = True
            if (base_node.down_left_child.contains(x + radius, y) or
                    base_node.down_left_child.contains(x - radius, y) or
                    base_node.down_left_child.contains(x, y + radius) or
                    base_node.down_left_child.contains(x, y - radius)
            ):
                down_left = True

            if (upper_left and down_right) or (upper_right and down_left):
                entities += base_node.upper_right_child.get_leaves()
                entities += base_node.upper_left_child.get_leaves()
                entities += base_node.down_right_child.get_leaves()
                entities += base_node.down_left_child.get_leaves()
            else:
                if upper_right:
                    entities += base_node.upper_right_child.get_leaves()
                if upper_left:
                    entities += base_node.upper_left_child.get_leaves()
                if down_right:
                    entities += base_node.down_right_child.get_leaves()
                if down_left:
                    entities += base_node.down_left_child.get_leaves()
        else:
            entities = base_node.get_leaves()

        final_entities = []

        for entity in entities:
            if self.euclidean_distance(x, y, entity.x, entity.y) <= radius:
                final_entities.append(entity)

        return final_entities

    def euclidean_distance(self, x1, y1, x2, y2):
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    def find_node(self, x, y):
        if self.contains(x, y):
            if self.divided:
                if self.upper_left_child.contains(x, y):
                    return self.upper_left_child.find_node(x, y)
                elif self.upper_right_child.contains(x, y):
                    return self.upper_right_child.find_node(x, y)
                elif self.down_left_child.contains(x, y):
                    return self.down_left_child.find_node(x, y)
                elif self.down_right_child.contains(x, y):
                    return self.down_right_child.find_node(x, y)
            else:
                return self
        else:
            return None

    def get_leaves(self):
        entities = []
        if self.divided:
            entities += self.upper_right_child.get_leaves()
            entities += self.upper_left_child.get_leaves()
            entities += self.down_right_child.get_leaves()
            entities += self.down_left_child.get_leaves()
        else:
            return self.entities
        return entities

    def draw(self, screen, color):
        pygame.draw.rect(screen, color, pygame.Rect(self.x - self.w,
                                                    self.y - self.h, self.w * 2,
                                                    self.h * 2), 1)
        if self.divided:
            self.upper_left_child.draw(screen, color)
            self.upper_right_child.draw(screen, color)
            self.down_left_child.draw(screen, color)
            self.down_right_child.draw(screen, color)


if __name__ == '__main__':
    import random
    import pygame


    class Entity:
        def __init__(self, w, h, aid):
            self.x, self.y = (random.random() * w, random.random() * h)
            self.aid = aid

        def move(self):
            x = self.x + random.random() * 2 - 1
            y = self.y + random.random() * 2 - 1
            self.x, self.y = (x, y)


    w = 500
    h = 500

    pygame.init()
    random.seed(42)

    colors = {
        'magenta': (1, 199, 200),
        'black': (0, 0, 0),
        'white': (255, 255, 255),
        'red': (255, 0, 0)
    }
    screen = pygame.display.set_mode((w, h))
    pygame.display.set_caption("Pandemic Simulator")

    exit_ = False
    quadTree = Node(w / 2, h / 2, w / 2, h / 2, 4)

    enti = []
    for i in range(100):
        enti.append(Entity(w, h, i))

    for i in enti:
        quadTree.insert(i)

    for i in quadTree.find_neighbors(250, 250, 100, ):
        print(i.x, i.y)

    while not exit_:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_ = True

        screen.fill(colors['black'])
        for i in enti:
            pygame.draw.circle(screen, colors['white'], (int(i.x), int(i.y)), 1)

        quadTree.draw(screen, colors['red'])

        pygame.display.update()

        quadTree = Node(w / 2, h / 2, w / 2, h / 2, 4)
        for i in enti:
            quadTree.insert(i)
