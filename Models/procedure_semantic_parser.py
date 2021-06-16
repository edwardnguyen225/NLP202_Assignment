from Models.data import WHS


WH_TO_PROC_SEM = {
    "WH-BUS": "PRINT-BUS ?b",
    "WH-RUNTIME": "PRINT-RUNTIME ?rt",
    "WH-TIME": "PRINT-TIME ?t",
    "WH-CITY": "PRINT-CITY ?c",
}


class Bus():
    def __init__(self, bus_code=None):
        self.set_bus_code(bus_code)

    def __str__(self):
        return f'(BUS {self.bus_code})'

    def set_bus_code(self, bus_code):
        self.bus_code = bus_code if bus_code else "?b"

    def get_bus_code(self):
        return self.bus_code


class BaseTime(Bus):
    def __init__(self, bus_code=None, place=None, hour=None):
        super().set_bus_code(bus_code)
        self.set_place(place)
        self.set_hour(hour)

    def __str__(self):
        return f'({self.bus_code} {self.place} {self.hour})'

    def set_place(self, place):
        self.place = place if place else "?c"

    def get_place(self):
        return self.place

    def set_hour(self, hour):
        self.hour = hour if hour else "?t"

    def get_hour(self):
        return self.hour


class Dtime(BaseTime):
    def __init__(self, bus_code=None, departure=None, hour=None):
        super().__init__(bus_code, departure, hour)

    def __str__(self):
        return f'(DTIME {self.bus_code} {self.place} {self.hour})'


class Atime(BaseTime):
    def __init__(self, bus_code=None, destination=None, hour=None):
        super().__init__(bus_code, destination, hour)

    def __str__(self):
        return f'(ATIME {self.bus_code} {self.place} {self.hour})'


class ProcedureSemanticParser():
    def __init__(self, logical_relations):
        self.logical_relations = logical_relations
        self.wh_query = None
        self.bus = Bus()
        self.dtime = Dtime(self.bus.bus_code)
        self.atime = Atime(self.bus.bus_code)
        self.set_procedure_semantic()

    def set_procedure_semantic(self):
        for relation in self.logical_relations:
            if relation.relation_name == "BUS-NP":
                bus_code = relation.child.word
                self.bus.set_bus_code(bus_code)
                self.dtime.set_bus_code(bus_code)
                self.atime.set_bus_code(bus_code)
            elif relation.relation_name == "FROM-LOC":
                loc = relation.child.word
                self.dtime.set_place(loc)
            elif relation.relation_name == "FROM-TIME":
                loc = relation.child.word
                self.dtime.set_hour(loc)
            elif relation.relation_name == "TO-LOC":
                loc = relation.child.word
                self.atime.set_place(loc)
            elif relation.relation_name == "TO-TIME":
                loc = relation.child.word
                self.atime.set_hour(loc)
            elif relation.relation_name in WHS:
                self.wh_query = WH_TO_PROC_SEM[relation.relation_name]
        self.procedure_semantic = [
            self.wh_query, self.bus, self.atime, self.dtime
        ]

    def get_procedure_semantic(self):
        return self.procedure_semantic

    def get_procedure_semantic_txt(self):
        return f'({self.wh_query} {self.bus}{self.atime}{self.dtime})'
