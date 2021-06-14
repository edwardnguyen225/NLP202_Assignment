import os
import sys
import random

from copy import copy
from Models.data import *
from Models.malt_parser import *
from Models.grammatical_relation import *
from Models.file_manipulator import *


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

    # ================= Malt Parser - Phân tích cú pháp phụ thuộc =================
    print("="*10, "Malt Parser - Phân tích cú pháp phụ thuộc", "="*10)
    question = preprocess(question)
    malt = MaltParser(question, my_lexicals, dependency_relations)
    malt.parse()
    malt_result = malt.get_malt()
    malt_txt = malt.get_malt_txt()
    print(malt_txt)
    write_file(PATH_TO_OUTPUT_FILES["a"], malt_txt)

    # ================= Grammatical Relation - Quan hệ văn phạm =================
    print("="*10, "Grammatical Relation - Quan hệ văn phạm", "="*10)
    grammatical_relation = GrammaticalRelation(malt_result)
    relations = grammatical_relation.get_relations()
    relations_txt = grammatical_relation.get_relations_txt()
    print(relations_txt)
    write_file(PATH_TO_OUTPUT_FILES["b"], relations_txt)


if __name__ == "__main__":
    argv = sys.argv[1:]
    question = random.choice(DEFAULT_QUESTIONS) if (len(argv) < 1) else argv

    main(question)
