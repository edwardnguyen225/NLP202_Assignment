from copy import copy
from Models.data import ROOT, WHS, get_token_type

PRED = "PRED"


class RelationPRED():
    def __init__(self, var, pred):
        self.relation_name = PRED
        self.var = var
        self.pred = pred

    def __str__(self):
        str = f'({self.var} {PRED} {self.pred})'
        return str


class RelationWH():
    def __init__(self, var, relation_name):
        self.relation_name = relation_name
        self.var = var

    def __str__(self):
        str = f'({self.var} {self.relation_name})'
        return str


class Relation():
    def __init__(self, var_parent, relation_name, var_child, child):
        self.var_parent = var_parent
        self.relation_name = relation_name
        self.var_child = var_child
        self.child = child
        self.child_type = get_token_type(child)

    def __str__(self):
        str = f'({self.var_parent} {self.relation_name} ({self.child_type} {self.var_child} {self.child}))'
        return str


class GrammaticalRelationParser():
    def __init__(self, malt):
        self.grammatical_relation = self.malt_to_grammatical_relation(malt)
        pass

    def get_relations(self):
        return self.grammatical_relation

    def get_relations_txt(self):
        result = ""
        for relation in self.grammatical_relation:
            row = str(relation) + "\n"
            result += row
        return result

    @staticmethod
    def malt_to_grammatical_relation(malt):
        malt_tree = copy(malt)
        relations_output = []
        variables = {}
        queue = [ROOT]
        while queue:
            """
            Pop the head of the queue
            Add all of its children to the queue
                and their relation, then remove it from malt_tree to make it easier to traverse latter
            """
            node = queue.pop(0)
            for relation_tup in malt_tree:
                if node != relation_tup[0]:
                    continue

                child = relation_tup[1]
                queue.append(child)
                variables[child] = f's{len(variables) + 1}'

                var = variables[child]
                relation_name = malt_tree[relation_tup]
                if relation_name == "PRED":
                    # relation = f'({var} PRED {child})'
                    relation = RelationPRED(var, child)
                elif relation_name in WHS:
                    var_parent = variables[node]
                    relation = RelationWH(var_parent, relation_name)
                else:
                    var_parent = variables[node]
                    relation = Relation(
                        var_parent, relation_name, var, child)
                relations_output.append(relation)
        return relations_output
