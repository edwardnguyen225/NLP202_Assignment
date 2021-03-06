from copy import copy
import re
from Models.data import WHS
import Models.grammatical_relation_parser as grammatical_relation_parser


relation_name_gramma_in_logical = {
    "LSUBJ": "AGENT",
    "LOBJ": "THEME"
}


class RelationBase(grammatical_relation_parser.RelationBase):
    pass


class RelationPRED(grammatical_relation_parser.RelationPRED):
    def __init__(self, var, predicate):
        super().__init__(var, predicate)

    def __str__(self):
        return f'({self.predicate} {self.var})'


class RelationWH(grammatical_relation_parser.RelationWH):
    def __init__(self, relation_name, var):
        super().__init__(relation_name, var)

    def __str__(self):
        return f'({self.relation_name} {self.var})'


class RelationParentChild(grammatical_relation_parser.RelationParentChild):
    def __init__(self, relation_name, var, child):
        if relation_name in relation_name_gramma_in_logical:
            self.relation_name = relation_name_gramma_in_logical[relation_name]
        else:
            self.relation_name = relation_name
        self.var = var
        if not isinstance(child, grammatical_relation_parser.RelationBase):
            raise TypeError(
                "Invalid grammatical relation child type: %s" % child.__class__.__name__)
        self.child = child

    def __str__(self):
        return f'({self.relation_name} {self.var} {self.child})'


class LogicalParser():
    def __init__(self, grammatical_relations, variables):
        self.variables = variables
        self.logical_relations = LogicalParser.gramma_to_logical_relations(
            grammatical_relations)
        self.logical_form_str = self.set_logical_form()

    def get_relations(self):
        return self.logical_relations

    def set_logical_form(self):
        relations = copy(self.get_relations())
        pred_relation = relations.pop(0)
        logical_form = f'{pred_relation.predicate} {pred_relation.var} '
        while relations:
            relation = relations.pop(0)
            if relation.relation_name in WHS:
                wh_query = relation.relation_name
                continue
            relation_str = str(relation)
            length = len(relation_str)
            relation_str = "\n\t[" + relation_str[1:length - 1] + "]"
            logical_form += relation_str

        logical_form = f'({logical_form})'
        if wh_query:
            logical_form = wh_query + logical_form

        return logical_form

    def get_logical_form(self):
        return self.logical_form_str

    @staticmethod
    def gramma_to_logical_relations(grammatical_relations):
        logical_relations = []
        for relation in grammatical_relations:
            new_logical_relation = LogicalParser.gramma_to_logical(relation)
            if new_logical_relation:
                logical_relations.append(new_logical_relation)
        return logical_relations

    @staticmethod
    def gramma_to_logical(gramma_relation):
        if not isinstance(gramma_relation, grammatical_relation_parser.RelationBase):
            raise TypeError("Invalid grammatical relation: %s" %
                            gramma_relation)

        relation = None
        if isinstance(gramma_relation, grammatical_relation_parser.RelationPRED):
            relation = RelationPRED(
                gramma_relation.var, gramma_relation.predicate)
        elif isinstance(gramma_relation, grammatical_relation_parser.RelationParentChild):
            relation_name = gramma_relation.relation_name
            relation = RelationParentChild(
                relation_name, gramma_relation.var, gramma_relation.child)
        elif isinstance(gramma_relation, grammatical_relation_parser.RelationWH):
            relation = RelationWH(
                gramma_relation.relation_name, gramma_relation.var)
        return relation
