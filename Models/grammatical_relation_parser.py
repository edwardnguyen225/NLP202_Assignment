from re import sub
from Models.malt_parser import MaltParser
from copy import copy
from Models.data import GAP, ROOT, WHS, get_token_type

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
        self.processed_malt_tree = GrammaticalRelationParser.process_malt_tree(
            malt)
        self.variables = self.set_variables()
        self.grammatical_relation = self.set_grammatical_relation_from_malt()

    def get_relations(self):
        return self.grammatical_relation

    def get_relations_txt(self):
        result = ""
        for relation in self.grammatical_relation:
            row = str(relation) + "\n"
            result += row
        return result

    def set_variables(self):
        malt_tree = self.processed_malt_tree

        variables = {
            "BUS": {"prefix": "b"},
            "BUS-CODE": {"prefix": "bn"},
            "CITY-NAME": {"prefix": "c"},
            "TIME-MODE": {"prefix": "t"},
            "OTHER": {"prefix": "s"}
        }
        queue = [ROOT]
        while queue:
            """
            Pop the head of the queue
            Add all of its children to the queue
                and their relation, then remove it from malt_tree to make it easier to traverse latter
            """
            node = queue.pop(0)
            for relation_tup in malt_tree.keys():
                if node != relation_tup[0]:
                    continue
                child = relation_tup[1]
                queue.append(child)
                child_type = get_token_type(child)
                if child_type not in variables:
                    child_type = "OTHER"
                sub_variables = variables[child_type]
                prefix = sub_variables["prefix"]
                variables[child_type][child] = f'{prefix}{len(variables[child_type])}'

        variables_output = {}
        for group in variables.values():
            for word, var in group.items():
                if word == "prefix":
                    continue
                variables_output[word] = var
        return variables_output

    def get_variables(self):
        return self.variables

    @staticmethod
    def process_malt_tree(malt):
        malt_tree_out = {}
        predicate = MaltParser.get_main_verb(malt)

        # Replace child in FROM-LOC, TO-LOC, and FROM-TIME, TO-TIME
        relations = list(malt.keys())
        count = 0
        while relations:
            relation_tup = relations.pop(0)
            relation_name = malt[relation_tup]
            if relation_name == "PREP":
                continue

            if relation_name in ["FROM-LOC", "TO-LOC"] and len(relations) > 0:
                next_relation_tup = relations[0]
                next_relation_name = malt[next_relation_tup]
                if next_relation_name in ["CITY-NP"]:
                    relation_tup = (predicate, next_relation_tup[1])
                    relations.pop(0)
                else:
                    relation_tup = (predicate, relation_tup[1])
            elif relation_name in ["FROM-LOC", "TO-LOC"]:
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

    def set_grammatical_relation_from_malt(self):
        malt_tree = self.processed_malt_tree

        relations_output = []
        variables = self.variables
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
        relations_output = self.replace_with_GAP(relations_output)
        return relations_output

    def replace_with_GAP(self, gramma_relations):
        copied_gramma_relations = copy(gramma_relations)
        wh_query = None
        lsubj_relation = None
        bus_np_relation = None
        for i in range(len(gramma_relations)):
            relation = gramma_relations[i]
            if relation.relation_name in WHS:
                wh_query = relation.relation_name
            elif relation.relation_name == "LSUBJ":
                lsubj_relation = relation
            elif relation.relation_name == "BUS-NP":
                bus_np_relation = relation
                bus_np_relation_index = i

        if bus_np_relation is not None:
            bus_code_relation = bus_np_relation.child
            bus_code_relation.var = bus_code_relation.word.lower()
            del self.variables[lsubj_relation.child.word]
            self.variables[bus_code_relation.word] = bus_code_relation.var

            lsubj_relation.child = bus_code_relation

            copied_gramma_relations.pop(bus_np_relation_index)
        else:
            child = RelationBase("BUS-CODE", lsubj_relation.child.var, GAP)
            lsubj_relation.child = child

        if wh_query == "WH-CITY":
            for relation in gramma_relations:
                count = 0
                for variable in self.variables.values():
                    if variable[0:1] == "c":
                        count += 1
                if relation.relation_name in ["FROM-LOC", "TO-LOC"] and relation.child.relation_name != "CITY-NAME":
                    count += 1
                    var = f'c{count}'
                    city = RelationBase("CITY-NAME", var, GAP)
                    relation.child = city

        return copied_gramma_relations
