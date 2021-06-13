import json


def write_file(path_to_file, data):
    try:
        f = open(path_to_file, "w", encoding='utf-8')
        f.write(data)
        f.close()
    except IOError:
        raise IOError


def relation_to_string(relation):
    left, right = relation
    str = f'({left}, {right})'
    return str


def malt_to_string(malt):
    result = ""
    for relation in malt:
        row = relation_to_string(relation)
        row += f': {malt[relation]}\n'
        result += row
    return result


def write_malt_to_file(path_to_file, malt):
    data = malt_to_string(malt)
    write_file(path_to_file, data)
