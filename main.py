import os
import sys
import random

from copy import copy
from Models.malt_parser import *
from Models.file_manipulator import *

DEFAULT_QUESTIONS = [
    "Xe bus nào đến thành phố Huế lúc 20:00HR ?",
    "Thời gian xe bus B3 từ Đà Nẵng đến Huế ?",
    "Xe bus nào đến thành phố Hồ Chí Minh ?",
    "Xe bus nào đến thành phố Hồ Chí Minh lúc 20:00HR ?"
]

REDUNDANT_TOKENS = [".", ",", "?", ":"]

PATH_TO_OUTPUT = os.path.join(".", "Output")
PATH_TO_OUTPUT_FILES = {
    "a": os.path.join(PATH_TO_OUTPUT, "output_a.txt"),
    "b": os.path.join(PATH_TO_OUTPUT, "output_b.txt"),
    "c": os.path.join(PATH_TO_OUTPUT, "output_c.txt"),
    "d": os.path.join(PATH_TO_OUTPUT, "output_d.txt"),
    "e": os.path.join(PATH_TO_OUTPUT, "output_e.txt"),
    "f": os.path.join(PATH_TO_OUTPUT, "output_f.txt"),
}

my_lexicals = {
    "bus": ["bus", "buýt", "xe_bus", "xe_buýt", "xe"],
    "city": ["city", "thành_phố", "tỉnh"],
    "arrive": ["đến", "tới"],
    "from": ["từ"],
    "wh": ["nào"],
    "atime": ["lúc", "vào_lúc"],
    "dtime": ["lúc", "từ_lúc"],
    "runtime": ["thời_gian"],
    "busname": ["B1", "B2", "B3", "B4", "B5", "B6"],
    "cityname": ["hue", "hcm", "hn", "danang", "hồ_chí_minh", "hà_nội", "huế", "đà_nẵng"],
    "time": ["time"]
}

# dependency from left --> right
dependency_relations = {
    "PRED": [("<ROOT>", "arrive")],
    "LSUBJ": [("arrive", "bus")],
    "PREP": [("arrive", "from")],
    "FROM-TIME": [
        ("from", "time"),
        ("dtime", "time")],
    "TO-TIME": [("atime", "time")],
    "PREP-TIME": [("arrive", "atime")],
    "FROM-LOC": [("from", "city")],
    "TO-LOC": [("arrive", "city")],
    "CITY": [("city", "cityname")],
    "BUS-NAME": [("busname", "bus")],
    "WH-BUS": [("bus", "wh")],
    "WH-RUN-TIME": [
        ("arrive", "runtime"),
        ("runtime", "wh")],
    "WH-FROM-TIME": [("dtime", "wh")],
    "WH-TO-TIME": [("atime", "wh")],
    "WH-CITY": [("city", "wh")],
}


def remove_redundant(str):
    result = copy(str)
    for token in REDUNDANT_TOKENS:
        result = result.replace(token, "")
    return result


def preprocess(str):
    result = copy(str)
    result = remove_redundant(result)
    result = " ".join(result.split())  # remove redundant whitespaces
    return result


def main(question):
    print("Your question: " + question)
    # ================= Malt Parser - Dependencies =================
    question = preprocess(question)
    malt = MaltParser(question, my_lexicals, dependency_relations)
    malt.parse()
    malt_result = malt.get_malt()
    print(malt_result)
    write_malt_to_file(PATH_TO_OUTPUT_FILES["a"], malt_result)


if __name__ == "__main__":
    argv = sys.argv[1:]
    question = random.choice(DEFAULT_QUESTIONS) if (len(argv) < 1) else argv

    question = "Xe bus nào đến thành phố Huế lúc 20:00HR ?"

    main(question)
