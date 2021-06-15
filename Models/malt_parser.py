from copy import copy
from pyvi import ViTokenizer
from Models.data import ROOT, TIME_MODE, get_token_type


LEFTARC = "LEFT-ARC"
RIGHTARC = "RIGHT-ARC"
REDUCE = "REDUCE"
SHIFT = "SHIFT"


def handle_splitting_xebus(tokens):
    tokens_result = copy(tokens)
    for i in range(len(tokens_result) - 2):
        if tokens_result[i].lower() == "xe" and tokens_result[i+1] == "bus":
            tokens_result[i] += "_bus"
            tokens_result.pop(i+1)
    return tokens_result


def fix_time_mode(tokens):
    tokens_result = copy(tokens)
    for i in range(len(tokens_result)):
        if get_token_type(tokens_result[i]) == TIME_MODE:
            token = tokens_result[i]
            token = f'{token[0:2]}:{token[2:]}'
            tokens_result[i] = token
    return tokens_result


def tokenize(str):
    tokens = ViTokenizer.tokenize(str).split()
    tokens = handle_splitting_xebus(tokens)
    tokens = fix_time_mode(tokens)
    return tokens


class MaltParser():
    def __init__(self, str, my_lexicals, rules):
        self.str = str
        self.my_lexicals = my_lexicals
        self.dependency_relations = rules
        self.tokens = tokenize(self.str)
        self.malt = {}

    def parse(self):
        self.stack = [ROOT]
        self.buffer = self.tokens
        self.malt = {}

        while self.buffer:
            (action, relation) = self.get_action_and_relation()
            if relation and (action != SHIFT or action != REDUCE):
                self.malt.update(relation)

            self.execute_action(action)

        del self.stack
        del self.buffer

        return

    def get_malt_txt(self):
        result = ""
        for relation in self.malt:
            row = self.relation_to_string(relation)
            row += f': {self.malt[relation]}\n'
            result += row
        return result

    def relation_to_string(self, relation):
        left, right = relation
        str = f'({left}, {right})'
        return str

    def get_malt(self):
        return self.malt

    def get_tokens(self):
        return self.tokens

    @staticmethod
    def get_main_verb(malt):
        for relation, relation_name in malt.items():
            if relation_name == "PRED":
                return relation[1]

    def get_action_and_relation(self):
        exist_relation_stack_top2 = False
        relations = self.malt.keys()
        if len(self.stack) > 1:
            stack_head = self.stack[-1]
            stack_head_under = self.stack[-2]
            pair = (stack_head, stack_head_under)
            pair_reverse = (stack_head_under, stack_head)
            if pair in relations or pair_reverse in relations:
                exist_relation_stack_top2 = True

        # stack head
        left = self.stack[-1]
        left_type = get_token_type(left)

        # buffer first element
        right = self.buffer[0]
        right_type = get_token_type(right)

        relation_result = {}

        for relation_name, relation_list in self.dependency_relations.items():
            if (left_type, right_type) in relation_list:
                relation_result = {
                    (left, right): relation_name
                }
                return (RIGHTARC, relation_result)
            elif (right_type, left_type) in relation_list and not exist_relation_stack_top2:
                relation_result = {
                    (right, left): relation_name
                }
                return (LEFTARC, relation_result)

        # Checking whether REDUCE or SHIFT
        if len(self.buffer) == 0 or exist_relation_stack_top2:
            return (REDUCE, None)

        return (SHIFT, None)

    def execute_action(self, action):
        if action == LEFTARC or action == REDUCE:
            self.stack.pop()
        elif action == RIGHTARC or action == SHIFT:
            self.stack.append(self.buffer[0])
            self.buffer.pop(0)
