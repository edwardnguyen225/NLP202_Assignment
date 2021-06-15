from copy import copy
from os.path import join
from re import search
from Models.bus import Bus

ROOT = "<ROOT>"
TIME_MODE = "TIME-MODE"

DEFAULT_QUESTIONS = [
    "Xe bus nào từ Hồ Chí Minh lúc 10:00HR đến thành phố Huế lúc 19:00HR ?",
    "Xe bus nào đến thành phố Huế lúc 20:00HR ?",
    "Thời gian xe bus B3 từ Đà Nẵng đến Huế ?",
    "Xe bus nào đến thành phố Hồ Chí Minh ?",
    "Xe bus nào đến thành phố Hồ Chí Minh lúc 20:00HR ?",
    "Xe bus B3 từ Đà Nẵng lúc 2030HR đến thành phố nào ?",
    "Xe bus B3 từ Đà Nẵng đến Huế lúc nào ?"
]

REDUNDANT_TOKENS = [".", ",", "?", ":"]

PATH_TO_INPUT = join(".", "Input")
PATH_TO_DATA_FILE = join(PATH_TO_INPUT, "database.txt")

PATH_TO_OUTPUT = join(".", "Output")
PATH_TO_OUTPUT_FILES = {
    "a": join(PATH_TO_OUTPUT, "output_a.txt"),
    "b": join(PATH_TO_OUTPUT, "output_b.txt"),
    "c": join(PATH_TO_OUTPUT, "output_c.txt"),
    "d": join(PATH_TO_OUTPUT, "output_d.txt"),
    "e": join(PATH_TO_OUTPUT, "output_e.txt"),
    "f": join(PATH_TO_OUTPUT, "output_f.txt"),
}

my_lexicals = {
    "BUS": ["bus", "buýt", "xe_bus", "xe_buýt", "xe"],
    "CITY": ["thành_phố", "tỉnh"],
    "BUS-ARRIVE": ["đến", "tới"],
    "FROM": ["từ"],
    "WH": ["nào"],
    "WH-TIME": ["lúc_nào"],
    "POINT-TIME": ["lúc", "vào_lúc"],
    "BUS-RUNTIME": ["thời_gian"],
    "BUS-CODE": ["B1", "B2", "B3", "B4", "B5", "B6"],
    "CITY-NAME": ["hue", "hcm", "hn", "danang", "hồ_chí_minh", "hà_nội", "huế", "đà_nẵng"],
    TIME_MODE: [TIME_MODE]
}

# dependency from left --> right
dependency_relations = {
    "PRED": [(ROOT, "BUS-ARRIVE")],
    "LSUBJ": [("BUS-ARRIVE", "BUS")],
    "PREP": [("BUS-ARRIVE", "FROM")],
    "AT-TIME": [("FROM", TIME_MODE), ("POINT-TIME", TIME_MODE)],
    "FROM-TIME": [("FROM", "POINT-TIME")],
    "TO-TIME": [("BUS-ARRIVE", "POINT-TIME")],
    "FROM-LOC": [("FROM", "CITY"), ("FROM", "CITY-NAME")],
    "TO-LOC": [("BUS-ARRIVE", "CITY"), ("BUS-ARRIVE", "CITY-NAME")],
    "CITY-NP": [("CITY", "CITY-NAME")],
    "BUS-NP": [("BUS", "BUS-CODE")],
    "WH-BUS": [("BUS", "WH")],
    "WH-RUNTIME": [
        ("BUS-ARRIVE", "BUS-RUNTIME"),
        ("BUS-RUNTIME", "WH")],
    "WH-TIME": [("BUS-ARRIVE", "WH-TIME")],
    "WH-CITY": [("CITY", "WH")],
}

WHS = ["WH-BUS", "WH-RUNTIME", "WH-TIME", "WH-CITY"]

BUS_DATA = {}


def get_token_type(word):
    for token_type in my_lexicals:
        token_type_list = list(
            map(lambda x: x.lower(), my_lexicals[token_type]))
        if word.lower() in token_type_list:
            return token_type
    time = copy(word)
    time = time.replace(":", "").lower()
    if search("\d{3,4}hr", time):
        return TIME_MODE
    elif word == ROOT:
        return ROOT
    return None


def remove_brackets_and_spaces(str):
    result = " ".join(str.split())
    result = result.replace("(", "")
    result = result.replace(")", "")
    return result


def row_to_list(row):
    lst = row.split(")")
    lst.remove("\n")
    lst = list(map(remove_brackets_and_spaces, lst))
    return lst


def load_bus_data():
    txt = ""
    with open(PATH_TO_DATA_FILE, "r") as f:
        txt = f.readlines()

    raw_data = []
    for row in txt:
        raw_data.extend(row_to_list(row))

    for data in raw_data:
        process_data(data)


def process_data(data):
    vals = data.split(" ")
    if vals[0].upper() == "BUS":
        set_bus(vals[1])
    elif vals[0].upper() == "ATIME":
        set_arrival(vals[1:])
    elif vals[0].upper() == "DTIME":
        set_departure(vals[1:])
    elif vals[0].upper() == "RUN-TIME":
        set_runtime(vals[1:])


def set_bus(bus_code):
    if bus_code in BUS_DATA:
        return
    new_bus = Bus(bus_code)
    BUS_DATA[bus_code] = new_bus


def set_arrival(lst):
    bus_code, dest, atime = lst
    if bus_code not in BUS_DATA:
        raise Exception("Unknown bus code: %s" % bus_code)

    bus = BUS_DATA[bus_code]
    bus.set_dest(dest)
    bus.set_atime(atime)


def set_departure(lst):
    bus_code, src, dtime = lst
    if bus_code not in BUS_DATA:
        raise Exception("Unknown bus code: %s" % bus_code)

    bus = BUS_DATA[bus_code]
    bus.set_src(src)
    bus.set_dtime(dtime)


def set_runtime(lst):
    if lst[-1].upper() == "HR":
        lst[-2] += lst[-1]
        lst.pop(-1)

    bus_code, src, dest, runtime = lst
    if bus_code not in BUS_DATA:
        raise Exception("Unknown bus code: %s" % bus_code)

    bus = BUS_DATA[bus_code]
    if bus.get_src() != src:
        raise Exception(f'Invalid bus {bus_code} source: {src}')
    elif bus.get_dest() != dest:
        raise Exception(f'Invalid bus {bus_code} destination: {dest}')

    bus.set_runtime(runtime)


def print_buses():
    for bus in BUS_DATA:
        print(BUS_DATA[bus])


load_bus_data()
