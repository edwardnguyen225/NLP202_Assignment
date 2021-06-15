from Models.malt_parser import MaltParser
from copy import copy
from Models.data import ROOT, WHS, get_token_type

PRED = "PRED"


class RelationBase():
    def __init__(self, relation_name, var=None, word=None):
        self.relation_name = relation_name
        self.var = var
        self.word = word

    def __str__(self):
        if self.var and self.word:
            return f'({self.relation_name} {self.var} {self.word})'
        return f'({self.relation_name})'


class RelationPRED(RelationBase):
    def __init__(self, var, predicate):
        super().__init__(PRED)
        self.var = var
        self.predicate = predicate

    def __str__(self):
        str = f'({self.var} {PRED} {self.predicate})'
        return str


class RelationWH(RelationBase):
    def __init__(self, relation_name, var):
        super().__init__(relation_name)
        self.var = var

    def __str__(self):
        return f'({self.var} {self.relation_name})'


class RelationParentChild(RelationBase):
    def __init__(self, relation_name, var, child_var, child_word):
        super().__init__(relation_name)
        self.var = var
        child_type = get_token_type(child_word)
        self.child = RelationBase(
            child_type, var=child_var, word=child_word)

    def __str__(self):
        str = f'({self.var} {self.relation_name} {self.child})'
        return str


class GrammaticalRelationParser():
    def __init__(self, malt):
        self.grammatical_relation = GrammaticalRelationParser.malt_to_grammatical_relation(
            malt)
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
    def process_malt_tree(malt):
        malt_tree_out = {}
        predicate = MaltParser.get_main_verb(malt)

        # Replace child in FROM-LOC, TO-LOC, and FROM-TIME, TO-TIME
        relations = list(malt.keys())
        while relations:
            relation_tup = relations.pop(0)
            relation_name = malt[relation_tup]
            if relation_name == "PREP":
                continue

            if relation_name in ["FROM-LOC", "TO-LOC"]:
                next_relation_tup = relations[0]
                next_relation_name = malt[next_relation_tup]
                if next_relation_name in ["CITY-NP"]:
                    relation_tup = (predicate, next_relation_tup[1])
                    relations.pop(0)
                else:
                    relation_tup = (predicate, relation_tup[1])
            elif relation_name in ["FROM-TIME", "TO-TIME"]:
                next_relation_tup = relations[0]
                next_relation_name = malt[next_relation_tup]
                if next_relation_name in ["AT-TIME"]:
                    relation_tup = (predicate, next_relation_tup[1])
                    relations.pop(0)
            malt_tree_out[relation_tup] = relation_name

        # Bring PRED and BUS to the top
        malt_tree_in = copy(malt_tree_out)
        malt_tree_out = {}
        moved_pred = False
        for relation in malt_tree_in:
            if malt_tree_in[relation] == PRED:
                pred_relation = relation
                malt_tree_out[relation] = malt_tree_in[relation]
                moved_pred = True
                break
        if moved_pred:
            del malt_tree_in[pred_relation]

        moved_lsubj = False
        for relation in malt_tree_in:
            if malt_tree_in[relation] == "LSUBJ":
                lsubj_relation = relation
                malt_tree_out[relation] = malt_tree_in[relation]
                moved_lsubj = True
                break
        if moved_lsubj:
            del malt_tree_in[lsubj_relation]

        malt_tree_out.update(malt_tree_in)
        return malt_tree_out

    @staticmethod
    def malt_to_grammatical_relation(malt):
        malt_tree = GrammaticalRelationParser.process_malt_tree(malt)

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
            for relation_tup, relation_name in malt_tree.items():
                if node != relation_tup[0]:
                    continue
                child = relation_tup[1]
                queue.append(child)
                variables[child] = f's{len(variables) + 1}'

                var = variables[child]
                relation = None
                if relation_name == "PRED":
                    # relation = f'({var} PRED {child})'
                    relation = RelationPRED(var, child)
                elif relation_name in WHS:
                    var_parent = variables[node]
                    relation = RelationWH(relation_name, var_parent)
                else:
                    var_parent = variables[node]
                    relation = RelationParentChild(
                        relation_name, var_parent, var, child)

                if relation:
                    relations_output.append(relation)
        return relations_output
