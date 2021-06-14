from copy import copy
from os.path import join
from re import search

ROOT = "<ROOT>"
TIME_MODE = "TIME-MODE"

DEFAULT_QUESTIONS = [
    "Xe bus nào đến thành phố Huế lúc 20:00HR ?",
    "Thời gian xe bus B3 từ Đà Nẵng đến Huế ?",
    "Xe bus nào đến thành phố Hồ Chí Minh ?",
    "Xe bus nào đến thành phố Hồ Chí Minh lúc 20:00HR ?",
    "Xe bus B3 từ Đà Nẵng lúc 2030HR đến thành phố nào ?",
    "Xe bus B3 từ Đà Nẵng đến Huế lúc nào ?"
]

REDUNDANT_TOKENS = [".", ",", "?", ":"]

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
    "BUS-SRC": ["từ"],
    "WH": ["nào"],
    "WH-TIME": ["lúc_nào"],
    "BUS-ATIME": ["lúc", "vào_lúc"],
    "BUS-DTIME": ["lúc", "từ_lúc"],
    "BUS-RUNTIME": ["thời_gian"],
    "BUS-CODE": ["B1", "B2", "B3", "B4", "B5", "B6"],
    "CITY-NAME": ["hue", "hcm", "hn", "danang", "hồ_chí_minh", "hà_nội", "huế", "đà_nẵng"],
    TIME_MODE: [TIME_MODE]
}

# dependency from left --> right
dependency_relations = {
    "PRED": [("<ROOT>", "BUS-ARRIVE")],
    "LSUBJ": [("BUS-ARRIVE", "BUS")],
    "PREP": [("BUS-ARRIVE", "BUS-SRC")],
    "FROM-TIME": [
        ("BUS-SRC", TIME_MODE),
        ("BUS-DTIME", TIME_MODE)],
    "TO-TIME": [("BUS-ATIME", TIME_MODE)],
    "PREP-TIME": [("BUS-ARRIVE", "BUS-ATIME")],
    "FROM-LOC": [("BUS-SRC", "CITY"), ("BUS-SRC", "CITY-NAME")],
    "TO-LOC": [("BUS-ARRIVE", "CITY"), ("BUS-ARRIVE", "CITY-NAME")],
    "CITY-NP": [("CITY", "CITY-NAME")],
    "BUS-NP": [("BUS", "BUS-CODE")],
    "WH-BUS": [("BUS", "WH")],
    "WH-RUN-TIME": [
        ("BUS-ARRIVE", "BUS-RUNTIME"),
        ("BUS-RUNTIME", "WH")],
    "WH-TIME": [("BUS-ARRIVE", "WH-TIME")],
    # "WH-FROM-TIME": [("BUS-DTIME", "WH"), ("BUS-ARRIVE", "WH")],
    # "WH-TO-TIME": [("BUS-ATIME", "WH")],
    "WH-CITY": [("CITY", "WH")],
}


# BUS_DATA = load_bus_data()


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


def load_bus_data():
    data = {}
    return data
