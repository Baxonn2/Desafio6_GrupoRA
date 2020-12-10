from typing import List, Tuple
import pygame

class Data:

    __x: float
    __y: float

    def __init__(self, x, y):
        self.__x = x
        self.__y = y
    
    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

class Chart:

    # Contendio del grafico
    __data: List[Data]
    __max_x: float
    __max_y: float
    __min_x: float

    # Posicionamiento y dimensiones
    __position: List[float]
    __dimension: List[float]

    def __init__(self, position: List[float],
                 dimension: List[float]):
        self.__data = []
        self.__max_x = 10
        self.__min_x = 9
        self.__max_y = 10
        self.__position = position
        self.__dimension = dimension
        self.__escala_x = 1
        self.__escala_y = 1
        self.__target_escala_x = 1
        self.__target_escala_y = 1
        
        self.font = pygame.font.Font(None, 20)

    def add(self, data: Data):
        self.__data.append(data)
        
        if data.get_x() > self.__max_x:
            self.__max_x = data.get_x()

        if data.get_y() > self.__max_y:
            self.__max_y = data.get_y()
        
        # Actualizando escala
        w, h = self.__dimension
        self.__target_escala_x = w / (self.__max_x - self.__min_x)
        self.__target_escala_y = h / self.__max_y
        
        if len(self.__data) > 100:
            self.__data.pop(0)
            self.__min_x = self.__data[0].get_x()

    def draw(self, surface: pygame.surface.Surface):
        x, y = self.__position
        w, h = self.__dimension

        # pygame.draw.rect(surface, (44, 44, 44), (x, y, w, h))

        # * ? Optimize: esto se puede actualizar cuando se agrega un nuevo punto
        self.__escala_x += (self.__target_escala_x - self.__escala_x) / 10.0
        self.__escala_y += (self.__target_escala_y - self.__escala_y) / 10.0
        for i, data in enumerate(self.__data[:-1]):
            data_x = (data.get_x()-self.__min_x) * self.__escala_x + x
            data_y = h - data.get_y() * self.__escala_y + y
            next_data = self.__data[i+1]
            next_data_x = (next_data.get_x()-self.__min_x) * self.__escala_x + x
            next_data_y = h - next_data.get_y() * self.__escala_y + y

            pygame.draw.line(surface, (130, 130, 130), 
                            (data_x, data_y), (next_data_x, next_data_y), 1)
            # pygame.draw.circle(surface, (130, 130, 130), (data_x, data_y), 2)

        maximo = self.font.render(f"Max = {self.__max_y}", True, (100, 100, 100))
        surface.blit(maximo, (x, y + h))

        # Agregando valor del ultimo punto
        if len(self.__data) > 0:
            color = (150, 150, 150)
            next_data_y = h - self.__data[-1].get_y() * self.__escala_y + y
            data_y = self.__data[-1].get_y()
            actual = self.font.render(f"{data_y}", True, color)
            
            # Agregando linea guia
            pygame.draw.line(surface, color, (x, next_data_y), (x + w, next_data_y))

            # Agregando texto del valor maximo
            surface.blit(actual, (x, next_data_y + 3))
