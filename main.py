import sys
import random
import Models.file_manipulator

from copy import copy
from Models.malt_parser import *

DEFAULT_QUESTIONS = [
    "Xe bus nào đến thành phố Huế lúc 20:00HR ?",
    "Thời gian xe bus B3 từ Đà Nẵng đến Huế ?",
    "Xe bus nào đến thành phố Hồ Chí Minh ?",
]

REDUNDANT_TOKENS = [".", ",", "?", ":"]

my_lexicals = {
    "bus": ["bus", "buýt", "xe_bus", "xe_buýt", "xe"],
    "city": ["city", "thành_phố", "tỉnh"],
    "arrive": ["đến", "tới"],
    "from": ["từ"],
    "wh": ["nào"],
    "dtime": ["lúc", "từ_lúc"],
    "atime": ["lúc", "vào_lúc"],
    "runtime": ["thời_gian"],
    "name": ["B1", "B2", "B3", "B4", "B5", "B6", "hue", "hcm", "hn", "danang", "hồ_chi_minh", "hà_nội", "huế", "đà_nẵng"],
    "time": ["time"]
}

dependencies = []


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
    malt = malt_parser(question, my_lexicals, dependencies)
    print(malt)


if __name__ == "__main__":
    argv = sys.argv[1:]
    question = random.choice(DEFAULT_QUESTIONS) if (len(argv) < 1) else argv

    main(question)
