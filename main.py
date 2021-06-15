import os
import sys
import random

from copy import copy
from Models.data import *
from Models.malt_parser import MaltParser
from Models.grammatical_relation_parser import GrammaticalRelationParser
from Models.logical_parser import LogicalParser
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


def print_header(header):
    print("="*10, header, "="*10)


def main(question):
    print("Your question: " + question)

    # ================= A - Malt Parser - Phân tích cú pháp phụ thuộc =================
    print_header("A - Malt Parser - Phân tích cú pháp phụ thuộc")
    question = preprocess(question)
    malt = MaltParser(question, my_lexicals, dependency_relations)
    malt.parse()
    malt_result = malt.get_malt()
    malt_txt = malt.get_malt_txt()
    print(malt_txt)
    write_file(PATH_TO_OUTPUT_FILES["a"], malt_txt)

    # ================= B - ??? - Quan hệ ngữ nghĩa =================
    print_header("B - ??? - Quan hệ ngữ nghĩa")
    print()

    # ================= C - Grammatical Relation - Quan hệ văn phạm =================
    print_header("C - Grammatical Relation - Quan hệ văn phạm")
    grammatical_relation = GrammaticalRelationParser(malt_result)
    gramma_relations = grammatical_relation.get_relations()
    relations_txt = grammatical_relation.get_relations_txt()
    print(relations_txt)
    write_file(PATH_TO_OUTPUT_FILES["c"], relations_txt)
    # return

    # ================= D - Logical Form - Dạng luận lý =================
    print_header("D - Logical Form - Dạng luận lý")
    logical_parser = LogicalParser(gramma_relations)
    print("\nPLUS ULTRAAAAAAAAAAAAAAAA")

    logical_relations = logical_parser.get_relations()
    for i in range(0, len(logical_relations)):
        print(i, logical_relations[i])


if __name__ == "__main__":
    argv = sys.argv[1:]
    question = random.choice(DEFAULT_QUESTIONS) if (len(argv) < 1) else argv
    question = DEFAULT_QUESTIONS[0]
    main(question)
