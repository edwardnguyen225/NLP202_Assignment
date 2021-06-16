from copy import copy

GAP = "<GAP>"


class Bus():
    def __init__(self, bus_code, src=None, dtime=None, dest=None, atime=None, runtime=None):
        self.bus_code = bus_code
        self.set_src(src)
        self.set_dtime(dtime)
        self.set_dest(dest)
        self.set_atime(atime)
        self.set_runtime(runtime)

    def __str__(self):
        str = f'{self.bus_code} from {self.src} ({self.dtime}) to {self.dest} ({self.atime}) in {self.runtime}'
        return str

    def set_src(self, src):
        self.src = src

    def get_src(self):
        return self.src

    def set_dest(self, dest):
        self.dest = dest

    def get_dest(self):
        return self.dest

    def set_atime(self, atime):
        self.atime = atime if atime is not None and self.is_hour(
            atime) else None

    def get_atime(self):
        return self.atime

    def set_dtime(self, dtime):
        self.dtime = dtime if dtime is not None and self.is_hour(
            dtime) else None

    def get_dtime(self):
        return self.dtime

    def set_runtime(self, runtime):
        self.runtime = runtime if runtime is not None and self.is_hour(
            runtime) else None

    def get_runtime(self):
        return self.runtime

    @staticmethod
    def is_hour(hour):
        try:
            tmp_hour = copy(hour)
            tmp_hour = tmp_hour.lower()
            if tmp_hour.find("hr"):
                tmp_hour = tmp_hour.replace("hr", "")
            hour_digits, minute_digits = tmp_hour.split(":")

            hour_digits = int(hour_digits)
            minute_digits = int(minute_digits)
            if hour_digits < 0 or hour_digits > 24:
                return False
            elif minute_digits < 0 or minute_digits > 60:
                return False
            return True

        except:
            return False


class DummyBus(Bus):
    def __init__(self, bus_code=None, src=None, dtime=None, dest=None, atime=None, runtime=None):
        self.bus_code = bus_code if bus_code is not None and bus_code != GAP and bus_code != "?" else None
        super().set_src(src) if src != GAP else super().set_src(None)
        super().set_dtime(dtime) if dtime != GAP else super().set_dtime(None)
        super().set_dest(dest) if dest != GAP else super().set_dest(None)
        super().set_atime(atime) if atime != GAP else super().set_atime(None)
        super().set_runtime(runtime) if runtime != GAP else super().set_runtime(None)

    def __str__(self):
        str = f'Dummy_bus {self.bus_code} from {self.src} ({self.dtime}) to {self.dest} ({self.atime}) in {self.runtime}'
        return str

    def compare_real_bus(self, real_bus):
        if self.bus_code is not None and self.bus_code != real_bus.bus_code:
            return False
        elif self.src is not None and self.src != real_bus.src:
            return False
        elif self.dtime is not None and self.dtime != real_bus.dtime:
            return False
        elif self.dest is not None and self.dest != real_bus.dest:
            return False
        elif self.atime is not None and self.atime != real_bus.atime:
            return False
        elif self.runtime is not None and self.runtime != real_bus.runtime:
            return False
        return True
