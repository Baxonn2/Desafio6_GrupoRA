import random
import src.parameters.load_instance_file as load
from src.grapher import Grapher

import sys, getopt

QUADTREE_ALGORITHM = "quadtree"
DYNAMIC_GRID_ALGORITHM = "dynamic_grid"

def main(entities, infected, masks, quarantine, instance=None):

    if instance is not None:
        load.load_parameters(instance)

    grapher = Grapher(algorithm=DYNAMIC_GRID_ALGORITHM,quarantine_enabled=quarantine)

    # Agregando entidad infectada
    # Total, enfermos, probabilidad de usar mascarilla, cuarentena
    grapher.add_entities(entities, infected, masks)

    grapher.run()
    print("Fin del programa")


def main_wrapper(argv):
    seed = 42
    entities = 10
    face_masks = 0
    infected = 0
    quarantine = False
    instance = None

    try:
        opts, args = getopt.getopt(argv, "qhs:e:i:m:f:",
                                   ["seed=",
                                    "entities=",
                                    "infected=",
                                    "masks",
                                    "instance=",
                                    ])
    except getopt.GetoptError:
        print('main.py -s <seed> -e <entities> -i <infected> -m <masks prob> -f <instance>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('main.py -s <seed> -e <entities> -i <infected> -m <masks prob> -f <instance>')
            sys.exit()
        elif opt in ("-s", "--seed"):
            seed = arg
        elif opt in ("-e", "--entities"):
            entities = int(arg)
        elif opt in ("-i", "--infected"):
            infected = int(arg)
        elif opt in ("-m", "--masks-prob"):
            face_masks = float(arg)
        elif opt in ("-f", "--instance"):
            instance = arg
        elif opt in ("-q", "--quarantine"):
            quarantine = True

    random.seed(seed)

    main(entities, infected, face_masks, quarantine, instance)


if __name__ == "__main__":
    main_wrapper(sys.argv[1:])
