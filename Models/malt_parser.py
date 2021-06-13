import re
from pyvi import ViTokenizer


ROOT = "<ROOT>"
LEFTARC = "LEFT-ARC"
RIGHTARC = "RIGHT-ARC"
REDUCE = "REDUCE"
SHIFT = "SHIFT"


def handle_splitting_xebus(tokens):
    for i in range(len(tokens) - 2):
        if tokens[i].lower() == "xe" and tokens[i+1] == "bus":
            tokens[i] += "_bus"
            tokens.pop(i+1)
    return tokens


def tokenize(str):
    tokens = ViTokenizer.tokenize(str).split()
    tokens = handle_splitting_xebus(tokens)
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

        count = 0
        # print(self.buffer)
        tokens_type = list(map(lambda x: self.get_token_type(x), self.buffer))
        # print((tokens_type))
        # print(self.stack)
        while self.buffer:
            # print("\n=========" + str(count) + "========")

            left_type = self.get_token_type(self.stack[-1])
            right_type = self.get_token_type(self.buffer[0])
            (action, relation) = self.get_action_and_relation()
            if relation and (action != SHIFT or action != REDUCE):
                self.malt.update(relation)

            self.execute_action(action)

            # print(left_type, right_type, "=>", action, relation)
            # print(self.buffer)
            # print(self.stack)
            count += 1

        del self.stack
        del self.buffer

        return

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
        if re.search("\d{3,4}hr", word.lower()):
            return "time"
        elif word == ROOT:
            return ROOT
        return None

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
        left_type = self.get_token_type(left)

        # buffer first element
        right = self.buffer[0]
        right_type = self.get_token_type(right)

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
