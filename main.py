##############################################################
#
# Đại học Bách Khoa TPHCM
# Author: Nguyễn Trí Nhân
# Date finish: 06/18/2021
#
##############################################################

from Models.result_retriever import ResultRetriever
from Models.procedure_semantic_parser import ProcedureSemanticParser
import sys
import random

from copy import copy
from Models.data import *
from Models.malt_parser import MaltParser
from Models.grammatical_relation_parser import GrammaticalRelationParser
from Models.logical_parser import LogicalParser
from Models.file_manipulator import *


HEADER_LENGTH = 69
HORIZONTAL_BAR = "-" * HEADER_LENGTH


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
    space_num = round((HEADER_LENGTH - len(header)) / 2) - 1
    spaces = " " * space_num
    header = f'|{spaces}{header}{spaces}|'
    print(HORIZONTAL_BAR)
    print(header)
    print(HORIZONTAL_BAR)


def main(question):
    print(HORIZONTAL_BAR)
    print("Your question: " + question + "\n")

    # ================= A - Malt Parser - Phân tích cú pháp phụ thuộc =================
    print_header("A - Malt Parser - Phân tích cú pháp phụ thuộc")
    question = preprocess(question)
    malt = MaltParser(question, my_lexicals, dependency_relations)
    malt.parse()
    malt_result = malt.get_malt()
    malt_txt = malt.get_malt_txt()
    print(malt_txt)
    write_file(PATH_TO_OUTPUT_FILES["a"], malt_txt)

    # ================= B - Semantic Relation - Quan hệ ngữ nghĩa =================
    # print_header("B - Semantic Relation - Quan hệ ngữ nghĩa")
    # print()

    # ================= C - Grammatical Relation - Quan hệ văn phạm =================
    print_header("C - Grammatical Relation - Quan hệ văn phạm")
    grammatical_relation = GrammaticalRelationParser(malt_result)
    relations_txt = grammatical_relation.get_relations_txt()
    print(relations_txt)
    write_file(PATH_TO_OUTPUT_FILES["c"], relations_txt)

    # ================= D - Logical Form - Dạng luận lý =================
    print_header("D - Logical Form - Dạng luận lý")
    gramma_relations = grammatical_relation.get_relations()
    variables = grammatical_relation.get_variables()
    logical_parser = LogicalParser(gramma_relations, variables)
    logical_form = logical_parser.get_logical_form()
    print(logical_form, "\n")
    write_file(PATH_TO_OUTPUT_FILES["d"], logical_form)

    # ================= E - Procedure Semantics - Ngữ nghĩa thủ tục =================
    print_header("E - Procedure Semantics - Ngữ nghĩa thủ tục")
    logical_relations = logical_parser.get_relations()
    proc_sem_parser = ProcedureSemanticParser(logical_relations)
    proc_sem_txt = proc_sem_parser.get_procedure_semantic_txt()
    proc_sem_txt += "\n"
    print(proc_sem_txt)
    write_file(PATH_TO_OUTPUT_FILES["e"], proc_sem_txt)

    # ================= F - The Result - Kết quả truy vấn =================
    print_header("F - The Result - Kết quả truy vấn")
    proc_sem = proc_sem_parser.get_procedure_semantic()
    result_retriever = ResultRetriever(proc_sem)
    result = result_retriever.get_result()
    print("Result (Kết quả):", result)
    result_str = result_retriever.get_result_str() + "\n"
    write_file(PATH_TO_OUTPUT_FILES["f"], result_str)

    return result  # For testing purpose


if __name__ == "__main__":
    argv = sys.argv[1:]
    question_list = list(DEFAULT_QUESTIONS.keys())
    exit_code = False
    if len(argv) > 0:
        argv_0 = argv[0]
        try:
            num = int(argv_0)
            if num not in range(len(question_list)):
                print(f"Number input is out of index, must be between 0 and {len(question_list) - 1}")
                exit_code = True
            question = question_list[num]
        except:
            question = argv_0
    else:
        question = random.choice(question_list)

    if exit_code == True:
        exit(0)
    main(question)

    # question = list(DEFAULT_QUESTIONS.keys())[0]
    # result = main(question)
    # print("RESULT FROM DATA:", DEFAULT_QUESTIONS[question])
    # print("COMPARING:", result == DEFAULT_QUESTIONS[question])

    # for question in DEFAULT_QUESTIONS:
    #     result = main(question)
    #     if result != DEFAULT_QUESTIONS[question]:
    #         raise Exception("ERROR:", question,
    #                         f'{result} != {DEFAULT_QUESTIONS[question]}')

    # print("\n" + HORIZONTAL_BAR)
    # print("PROGRAM RUN SUCCESSFULLY WITHOUT ANY BUG 🍻")
