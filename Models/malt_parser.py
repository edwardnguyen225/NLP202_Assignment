import re
from copy import copy
from pyvi import ViTokenizer


def malt_parser(str, my_lexicals, rules):
    malt = {}
    sentence = copy(str)
    tokens = ViTokenizer.tokenize(sentence).lower().split()
    tokens = handle_splitting_xebus(tokens)

    return malt


def handle_splitting_xebus(tokens):
    for i in range(len(tokens) - 2):
        if tokens[i] == "xe" and tokens[i+1] == "bus":
            tokens[i] = "xe_bus"
            tokens.pop(i+1)
    return tokens


def get_token_type(word, my_lexicals):
    return None
