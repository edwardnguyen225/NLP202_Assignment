import Models.bus
import Models.procedure_semantic_parser as ProcSem

from copy import copy
from Models.data import BUS_DATA, GAP, get_city_realname

NO_BUS_FOUND = "Không tìm được xe bus thỏa điều kiện đã cho!"
NO_CITY_FOUND = "Không tìm được thành phố/tỉnh"
NOT_SET_RUN_TIME = "Thời gian chạy chưa được cài đặt"
WRONG_BUS_SRC_DEST = "Sai địa điểm khởi hành/kết thúc của xe bus"
SOMETHING_WRONG = "Lỗi thông tin xe bus"
SOMETHING_WRONG_WHEN_GET_TIME = SOMETHING_WRONG + " khi tìm thời gian"
SOMETHING_WRONG_WHEN_GET_SRC = SOMETHING_WRONG + " khi tìm nơi khởi hành"
SOMETHING_WRONG_WHEN_GET_DEST = SOMETHING_WRONG + " khi tìm nơi đến"


def create_dummy_bus(condition):
    bus_code = condition["bus"]
    src = get_city_realname(condition["src"])
    dtime = condition["dtime"]
    dest = get_city_realname(condition["dest"])
    atime = condition["atime"]
    runtime = condition["runtime"]
    dummy_bus = Models.bus.DummyBus(bus_code, src, dtime, dest, atime, runtime)
    return dummy_bus


class ResultRetriever():
    def __init__(self, proc_sem):
        self.set_proc_sem(proc_sem)
        self.condition = {
            "bus": None, "src": None, "dtime": None, "dest": None, "atime": None, "runtime": None
        }
        self.set_condition()
        self.set_result()

    def set_proc_sem(self, proc_sem):
        queue = copy(proc_sem)
        command = None
        self.bus = ProcSem.Bus()
        self.dtime = ProcSem.Dtime()
        self.atime = ProcSem.Atime()
        while len(queue) > 1:
            head = queue.pop(0)
            if isinstance(head, ProcSem.Dtime):
                self.dtime = copy(head)
            elif isinstance(head, ProcSem.Atime):
                self.atime = copy(head)
            elif isinstance(head, ProcSem.Bus):
                self.bus = copy(head)
            else:
                queue.append(head)
        self.command = queue.pop().split()[0]

    def set_condition(self):
        bus_code = self.bus.bus_code
        self.condition["bus"] = bus_code if bus_code != "?b" else None

        dtime = self.dtime
        self.condition["src"] = dtime.place if dtime.place != "?c" else None
        self.condition["dtime"] = dtime.hour if dtime.hour != "?t" else None

        atime = self.atime
        self.condition["dest"] = atime.place if atime.place != "?c" else None
        self.condition["atime"] = atime.hour if atime.hour != "?t" else None

        if self.command == "PRINT-BUS":
            self.condition["bus"] = "?"
        elif self.command == "PRINT-RUNTIME":
            self.condition["runtime"] = "?"
        elif self.command == "PRINT-TIME":
            if self.condition["dtime"] == None:
                self.condition["dtime"] = "?"
            if self.condition["atime"] == None:
                self.condition["atime"] = "?"
        elif self.command == "PRINT-CITY":
            if self.condition["src"] == None:
                self.condition["src"] = "?"
            if self.condition["dest"] == None:
                self.condition["dest"] = "?"

    def set_result(self):
        result = None
        if self.command == "PRINT-BUS":
            result = self.get_buses()
        elif self.command == "PRINT-RUNTIME":
            result = self.get_runtime()
        elif self.command == "PRINT-TIME":
            result = self.get_time()
        elif self.command == "PRINT-CITY":
            result = self.get_city()
        self.result = result

    def get_result(self):
        return self.result

    def get_result_str(self):
        if isinstance(self.result, str):
            return self.result
        result = "["
        for i in range(len(self.result)):
            result += self.result[i]
            result += ", " if i + 1 < len(self.result) else "]"
        return result

    def get_buses(self):
        result = []
        dummy_bus = create_dummy_bus(self.condition)

        for bus in BUS_DATA.values():
            if dummy_bus.compare_real_bus(bus) == True:
                result.append(bus.bus_code)
        return result if result else NO_BUS_FOUND

    def get_runtime(self):
        dummy_bus = create_dummy_bus(self.condition)

        bus_code = self.condition["bus"]

        if bus_code != None and bus_code != GAP and bus_code not in BUS_DATA:
            return NO_BUS_FOUND
        elif bus_code in BUS_DATA:
            real_bus = BUS_DATA[bus_code]
            if dummy_bus.compare_real_bus(real_bus):
                return real_bus.runtime
            return f'{WRONG_BUS_SRC_DEST} {bus_code}'

        result = []
        for bus in BUS_DATA.values():
            if dummy_bus.compare_real_bus(bus) == True:
                result.append(bus.runtime)
        if len(result) == 1:
            result = result.pop()
        return result if result else NOT_SET_RUN_TIME

    def get_time(self):
        dummy_bus = create_dummy_bus(self.condition)
        bus_code = self.condition["bus"]
        if bus_code != None and bus_code not in BUS_DATA:
            return NO_BUS_FOUND
        elif bus_code in BUS_DATA:
            real_bus = BUS_DATA[bus_code]
            if dummy_bus.compare_real_bus(real_bus):
                return real_bus.atime
        return SOMETHING_WRONG_WHEN_GET_SRC

    def get_city(self):
        result = ""
        if self.condition["src"] == GAP:
            result = self.get_src()
        elif self.condition["dest"] == GAP:
            result = self.get_dest()
        return result if result else NO_CITY_FOUND

    def get_src(self):
        dummy_bus = create_dummy_bus(self.condition)
        bus_code = self.condition["bus"]

        if bus_code == GAP:
            buses = self.get_buses()
            result = []
            for bus_code in buses:
                real_bus = BUS_DATA[bus_code]
                if dummy_bus.compare_real_bus(real_bus):
                    result.append(real_bus.dest)
            if len(result) == 1:
                result = result.pop()
            return result if result else SOMETHING_WRONG_WHEN_GET_SRC
        elif bus_code != None and bus_code not in BUS_DATA:
            return NO_BUS_FOUND
        elif bus_code in BUS_DATA:
            real_bus = BUS_DATA[bus_code]
            if dummy_bus.compare_real_bus(real_bus):
                return real_bus.src
        return SOMETHING_WRONG_WHEN_GET_SRC

    def get_dest(self):
        dummy_bus = create_dummy_bus(self.condition)
        bus_code = self.condition["bus"]
        if bus_code == GAP:
            buses = self.get_buses()
            result = []
            for bus_code in buses:
                real_bus = BUS_DATA[bus_code]
                if dummy_bus.compare_real_bus(real_bus):
                    result.append(real_bus.dest)
            if len(result) == 1:
                result = result.pop()
            return result if result else SOMETHING_WRONG_WHEN_GET_SRC
        elif bus_code != None and bus_code not in BUS_DATA:
            return NO_BUS_FOUND
        elif bus_code in BUS_DATA:
            real_bus = BUS_DATA[bus_code]
            if dummy_bus.compare_real_bus(real_bus):
                return real_bus.dest
        return SOMETHING_WRONG_WHEN_GET_DEST
