from .entity import Entity
import random
from src.search.quadtree import Node as Node
from src.dynamic_grid.dynamic_grid import DynamicGrid
from src.parameters import infection
import pygame

WORLD_WIDTH = 600
WORLD_HEIGHT = 600


class Population:

    def __init__(self, population=0, sick_entities=0, masks=0,
                 algorithm='quadtree', quarantine_enabled=True):
        self.entities = []
        self.sick_entities = {}
        self.healthy_entities = {}
        self.deads_entites = {}
        self.quarantine_enabled = quarantine_enabled
        self.current_iteration = 0
        self.__update_count = 0
        self.algorithm = algorithm

        # Creando dynamic grid
        self.dg = DynamicGrid()

        if population > 0 or sick_entities > 0:
            self.add_entities(population, sick_entities, masks)

    def add_entities(self, total_population: int, initial_sick: int,
                     mask: float = 0, quarantine=None):
        """
        Crea una poblacion de entidades.

        :param quarantine: activa o desactiva la cuarentena en
        :param total_population: cantidad total de entidades en la poblacion
        :param initial_sick: cantidad de entidades enfermas al inicio de la
                             propagacion de la enfermedad
        :param mask: probabilidad entre 0 y 1 de que una entidad use mascara
        """
        if quarantine is not None:
            self.quarantine_enabled = quarantine

        total_sick = 1
        if initial_sick > total_population:
            raise ValueError(
                "La cantidad de infectados es mayor al tamaño de la población")

        for i in range(total_population):
            # Posicion inicial de la entidad
            x, y = random.random() * WORLD_WIDTH, random.random() * WORLD_HEIGHT
            # Uso de mascara
            has_mask = mask > 0 and random.random() <= mask
            # Primero crea a los infectados y luego a los sanos
            entity = Entity(x, y, total_sick <= initial_sick, has_mask)
            total_sick += 1

            self.entities.append(entity)
            if entity.is_infected:
                self.sick_entities[entity.person_id] = entity
            else:
                self.healthy_entities[entity.person_id] = entity
                self.dg.add(x, y, entity)

    def update(self):
        """
        Actualiza y dibuja las entidades en pantalla
        """
        self.current_iteration += 1
        if self.algorithm == "quadtree":
            self.__update_quadtree()
        if self.algorithm == "dynamic_grid":
            self.__update_dynamic_grid()

    def __update_dynamic_grid(self):
        self.dg.update()

        new_infected = set()

        for infected_entity in self.sick_entities.values():
            if self.quarantine_enabled and \
                    infected_entity.sick_time > infection.DETECTION_DELAY:
                # se va a cuarnetena
                infected_entity.send_to_quarantine(WORLD_WIDTH, WORLD_HEIGHT)
                # como está en cuarentena no infecta
                continue

            entities = self.dg.get(infected_entity.x, infected_entity.y, infected_entity.radius())

            ids = []
            for i in entities:
                infected_entity.infect(i)
                if i.is_infected:
                    ids.append(i.person_id)

            new_infected.update(ids)


        for entity_id in new_infected:
            self.sick_entities[entity_id] = self.healthy_entities.pop(entity_id)
            entity = self.sick_entities[entity_id]
            self.dg.remove(entity.x, entity.y, entity)

    def __update_quadtree(self):
        # Buscando infectados
        self.quadtree = Node(WORLD_WIDTH / 2, WORLD_HEIGHT / 2,
                             WORLD_WIDTH / 2, WORLD_HEIGHT / 2, 3)

        for entity in self.healthy_entities.values():
            self.quadtree.insert(entity)
        new_infected = set()

        for infected_entity in self.sick_entities.values():

            if self.quarantine_enabled and \
                    infected_entity.sick_time > infection.DETECTION_DELAY:
                # se va a cuarnetena
                infected_entity.send_to_quarantine(WORLD_WIDTH, WORLD_HEIGHT)
                # como está en cuarentena no infecta
                continue

            entities = self.quadtree.find_neighbors(infected_entity.x,
                                                    infected_entity.y,
                                                    infected_entity.radius())
            ids = []
            for i in entities:
                infected_entity.infect(i)
                if i.is_infected:
                    ids.append(i.person_id)

            new_infected.update(ids)

        for entity_id in new_infected:
            self.sick_entities[entity_id] = self.healthy_entities.pop(
                entity_id)

    def update_entity(self, entity: Entity):
        """
        Actualiza la entidad ingresada como parametro. También infecta a todas
        las que esta entidad puede infectar.

        Args:
            entity (Entity): Entidad a actualizar.
        """
        # Actualizando entidad
        if entity.is_alive:
            infected = entity.is_infected
            entity.step()

            if entity.in_target() and not entity.is_at_quarentine:
                x, y = random.random() * WORLD_WIDTH, random.random() * WORLD_HEIGHT
                entity.set_target_position(x, y)
            if infected and not entity.is_infected:
                if self.quarantine_enabled:
                    entity.is_at_quarentine = False

                self.sick_entities.pop(entity.person_id)
                self.healthy_entities[entity.person_id] = entity

            if not entity.is_alive:
                self.deads_entites[entity.person_id] = entity

    def get_update_count(self) -> int:
        """
        Obtiene la cantidad de iteraciones que se han hecho.

        Returns:
            int: Cantidad de iteraciones realizadas.
        """
        return self.current_iteration

    def get_infected(self) -> int:
        return len(self.sick_entities)

    def get_healthy(self) -> int:
        return len(self.healthy_entities)

    def get_deads(self) -> int:
        return len(self.deads_entites)

    def draw_quadtree(self, surface: pygame.surface.Surface):
        self.quadtree.draw(surface, (111, 111, 111))

    def draw_dynamic_grid(self, surface: pygame.surface.Surface):
        self.dg.draw(surface, (111, 111, 111))