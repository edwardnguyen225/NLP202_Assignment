import re
from pyvi import ViTokenizer


def handle_splitting_xebus(tokens):
    for i in range(len(tokens) - 2):
        if tokens[i] == "xe" and tokens[i+1] == "bus":
            tokens[i] = "xe_bus"
            tokens.pop(i+1)
    return tokens


def tokenize(str):
    tokens = ViTokenizer.tokenize(str).lower().split()
    tokens = handle_splitting_xebus(tokens)
    return tokens


class MaltParser():
    def __init__(self, str, my_lexicals, rules):
        self.str = str
        self.my_lexicals = my_lexicals
        self.rules = rules
        self.tokens = tokenize(self.str)
        self.malt = {}

    def parse(self):
        tokens_type = list(
            map(lambda x: self.get_token_type(x), self.tokens))

    def get_malt(self):
        return self.malt

    def get_tokens(self):
        return self.tokens

    def get_token_type(self, word):
        for token_type in self.my_lexicals:
            token_type_list = list(
                map(lambda x: x.lower(), self.my_lexicals[token_type]))
            if word.lower() in token_type_list:
                return token_type
        if re.search("\d{3,4}hr", word):
            return "time"
        return None
