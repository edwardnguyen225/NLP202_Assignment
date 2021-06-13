from posixpath import lexists
import re
from copy import copy
from pyvi import ViTokenizer


def malt_parser(str, my_lexicals, rules):
    malt = {}
    sentence = copy(str)
    tokens = ViTokenizer.tokenize(sentence).lower().split()
    tokens = handle_splitting_xebus(tokens)
    tokens_type = list(map(lambda x: get_token_type(x, my_lexicals), tokens))

    return malt


def handle_splitting_xebus(tokens):
    for i in range(len(tokens) - 2):
        if tokens[i] == "xe" and tokens[i+1] == "bus":
            tokens[i] = "xe_bus"
            tokens.pop(i+1)
    return tokens


def get_token_type(word, my_lexicals):
    for token_type in my_lexicals:
        token_type_list = list(
            map(lambda x: x.lower(), my_lexicals[token_type]))
        if word.lower() in token_type_list:
            return token_type
    if re.search("\d{3,4}hr", word):
        return "time"
    return None
