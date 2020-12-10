import random
from math import sqrt, pow
from .parameters import infection
from .parameters.status import (HEALTHY, HEALTHY_MASK, INFECTED, INFECTED_MASK,
                                IMMUNE, IMMUNE_MASK, DEAD)


class Entity:
    # Constantes de posicionamiento
    TARGET_DONE_RANGE = 0.5
    PERSON_ID = 0

    def __init__(self, x, y, is_infected=False, has_mask=False):
        Entity.PERSON_ID += 1
        self.x = x
        self.y = y
        self.z = None
        self.person_id = Entity.PERSON_ID

        self._x_target = x
        self._y_target = y
        self._z_target = None
        self._target_done = True

        self.is_infected = is_infected
        self.is_recovered = False
        self.is_immune = False
        self.is_alive = True
        self.is_at_quarentine = False
        self.has_mask = has_mask

        self.sick_time = 0
        self.immunity_time = 0

    def step(self):
        """
        Mueve la posicion de la entidad a su posicion objetivo
        """
        if self.is_alive:
            dx = (self._x_target - self.x) / 20
            dy = (self._y_target - self.y) / 20

            MAX = 1

            if abs(dx) > MAX:
                dx = MAX if dx > 0 else -MAX
            if abs(dy) > MAX:
                dy = MAX if dy > 0 else -MAX

            self.x += dx
            self.y += dy

            # Actualizando el estado del target
            self._target_done = abs(dx) < self.TARGET_DONE_RANGE and \
                abs(dy) < self.TARGET_DONE_RANGE

            self.update_status()

    def update(self):
        self.step()
        return self.x, self.y

    def set_target_position(self, x: float, y: float):
        """
        Actualiza la posicion objetivo de la entidad a las coordenadas entregadas

        :param x: Posicion X en el mapa
        :param y: Posicion y en el mapa
        """
        self._x_target = x
        self._y_target = y

    def in_target(self):
        """
        Comprueba si la entidad se encuentra en su posicion objetivo.

        :return: True si esta en el objetivo.
        """
        return self._target_done

    def radius(self):
        """
        Calculo del radio de infeccion de la entidad.

        :return:
        """
        if self.has_mask:
            return infection.INFECT_RADIUS * infection.MASK_RADIUS_INFECTION
        return infection.INFECT_RADIUS

    def update_status(self):
        """
        Actualiza el estado actual de la entidad. Comprueba si continua enfermo,
        ha fallecido, se ha recuperado o se encuentra en un estado de inmunidad.

        :return:
        """
        if self.is_infected:
            self.sick_time += 1
            probability = random.random()
            # Calculo de probabilidad de morir luego de haber sobrevivido el 70%
            # de la enfermedad
            if self.dead_by_infection():
                self.is_alive = False
                self.is_infected = False
            # Probabilidad de curarse antes del tiempo esperado
            elif probability <= infection.RECOVERY_BEFORE_TIME:
                self.is_infected = False
            # Probabilidad de curarse luego del tiempo estimado para la
            # enfermedad
            elif self.sick_time >= infection.SICKNESS_DURATION and \
                    probability <= infection.RECOVERY_AFTER_TIME:
                self.is_infected = False

            # Si ha dejado de estar infectad y sobrevive a la enfermedad,
            # entonces gana el estado de inmunidad por N iteraciones
            if not self.is_infected and self.is_alive:
                self.sick_time = 0
                self.is_immune = True
                self.is_recovered = True

        # Actualizacion del estado de inmunidad
        if self.is_immune:
            self.immunity_time += 1

            if self.immunity_time >= infection.IMMUNITY_DURATION:
                if random.random() <= infection.IMMUNITY_PROB_AFTER_TIME:
                    self.immunity_time = 0
                    self.is_immune = False

    def dead_by_infection(self):
        if infection.DEATH_PROB == 0:
            return False
        probability = ((8 * pow((infection.SICKNESS_DURATION /
                                 (2 * infection.DIFF_PROB)), 3) /
                        (pow((self.sick_time - (
                            infection.SICKNESS_DURATION / 2)), 2) +
                         4 * pow((infection.SICKNESS_DURATION /
                                  (infection.DIFF_PROB * 2)), 2)))) / \
                      (infection.SICKNESS_DURATION /
                       (infection.DIFF_PROB * infection.DEATH_PROB))

        # probability = (8 * pow(DEATH_PROB, 3) /
        #                (pow((self.sick_time - SICKNESS_DURATION), 2) +
        #                 4 * pow(DEATH_PROB, 2)))
        return random.random() <= probability

    def infect(self, entity):
        """
        Funcion encargada de infectar a otra entidad si es que esta dentro del
        rango y la probabilidad fue suficiente

        :param entity: Otra entidad a infectar
        """
        if not self.is_infected or not self.is_alive:
            return
        if entity.is_infected or not entity.is_alive:
            return

        x2, y2 = entity.x, entity.y

        distance = sqrt((self.x - x2) ** 2 + (self.y - y2) ** 2)

        infection_value = infection.INFECT_PROB
        if entity.is_immune:
            infection_value *= infection.IMMUNITY_FAIL
        if entity.has_mask:
            infection_value *= infection.MASK_FACTOR_HEALTHY
        if self.has_mask:
            infection_value *= infection.MASK_FACTOR_SICK
        if entity.is_recovered:
            infection_value *= infection.RECOVERED_FACTOR

        # La probabilidad de infectarse depende del radio de infeccion de la
        # entidad infecciosa. Este radio cambia si la entidad tiene mascarilla
        # a medida que la distancia sea mayor, menos probabilidades la otra
        # entidad tendra de contagiarse
        if distance < self.radius() and random.random() <= infection_value:
            if random.random() >= distance / self.radius():
                entity.is_infected = True

    def send_to_quarantine(self, width, height):
        if self.is_at_quarentine:
            if self.in_target():
                x = width * (1.1 + random.random() * 0.3)
                y = height * (0.55 + random.random() * 0.3)
                self.set_target_position(x, y)
        else:
            self.x = width * (1.05 + random.random() * 0.4)
            self.y = height * (0.5 + random.random() * 0.4)

            self.set_target_position(self.x, self.y)
            self.is_at_quarentine = True

    def get_status(self):
        radius = infection.INFECT_RADIUS
        infecting = False
        if self.is_alive:
            if self.is_infected:
                color = INFECTED
                if self.has_mask:
                    color = INFECTED_MASK
                    radius = infection.INFECT_RADIUS * \
                        infection.MASK_RADIUS_INFECTION
            elif self.is_immune:
                color = IMMUNE
                if self.has_mask:
                    color = IMMUNE_MASK
            else:
                color = HEALTHY
                if self.has_mask:
                    color = HEALTHY_MASK
        else:
            color = DEAD

        casted_position = [int(self.x), int(self.y)]

        if self.is_infected and random.random() < infection.INFECT_PROB:
            infecting = True

        return [color, infecting, casted_position, radius]


if __name__ == '__main__':
    person1 = Entity(0, 0)
    person2 = Entity(1, 0, is_infected=True)
    person3 = Entity(1, 1, has_mask=True)

    print(f'ID de las personas\n{person1.person_id}\n{person2.person_id}'
          f'\n{person3.person_id}')
    while not person1.is_infected:
        print('contagiando a personas')
        person2.infect(person1)
        person2.infect(person3)
