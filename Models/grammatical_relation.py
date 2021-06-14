from copy import copy
from Models.data import ROOT, get_token_type


class GrammaticalRelation():
    def __init__(self, malt):
        self.grammatical_relation = self.malt_to_grammatical_relation(malt)
        pass

    def get_relations(self):
        return self.grammatical_relation

    def get_relations_txt(self):
        result = ""
        for relation in self.grammatical_relation:
            row = relation + "\n"
            result += row
        return result

    @staticmethod
    def malt_to_grammatical_relation(malt):
        malt_tree = copy(malt)
        relations_output = []
        variables = {}
        queue = [ROOT]
        count = 0
        while queue:
            count += 1
            """
            Pop the head of the queue
            Add all of its children to the queue
                and their relation, then remove it from malt_tree to make it easier to traverse latter
            """
            node = queue.pop(0)
            for relation_tup in malt_tree:
                if node == relation_tup[0]:
                    child = relation_tup[1]
                    queue.append(child)
                    variables[child] = f's{len(variables) + 1}'

                    var = variables[child]
                    relation_name = malt_tree[relation_tup]
                    if relation_name == "PRED":
                        relation = f'({var} PRED {child})'
                    elif relation_name in ["WH-BUS", "WH-RUN-TIME"]:
                        relation = f"({relation_name} {var})"
                    else:
                        var_parent = variables[node]
                        relation = f"({var_parent} {relation_name} ({get_token_type(child)} {var} {child}))"
                    relations_output.append(relation)

        return relations_output
