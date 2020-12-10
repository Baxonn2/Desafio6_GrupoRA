from src.parameters import infection
from pprint import pprint
import json


def load_parameters(filename):
    with open(filename, 'r') as fh:
        data = json.load(fh)

    for key, value in data.items():
        infection.__dict__[key] = value

