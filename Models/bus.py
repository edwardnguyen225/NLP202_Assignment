from copy import copy


class Bus():
    def __init__(self, bus_code):
        self.bus_code = bus_code
        self.src = None
        self.dtime = None

        self.dest = None
        self.atime = None

        self.runtime = None

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
        if self.is_hour(atime):
            self.atime = atime

    def get_atime(self):
        return self.atime

    def set_dtime(self, dtime):
        if self.is_hour(dtime):
            self.dtime = dtime

    def get_dtime(self):
        return self.dtime

    def set_runtime(self, runtime):
        if self.is_hour(runtime):
            self.runtime = runtime

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
            raise ValueError("Invalid hour")
