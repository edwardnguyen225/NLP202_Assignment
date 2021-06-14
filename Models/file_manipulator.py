import json
from Models.malt_parser import MaltParser


def write_file(path_to_file, data):
    try:
        f = open(path_to_file, "w", encoding='utf-8')
        f.write(data)
        f.close()
    except IOError:
        raise IOError
