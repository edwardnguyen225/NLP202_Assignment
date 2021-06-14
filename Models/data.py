from os.path import join

ROOT = "<ROOT>"


DEFAULT_QUESTIONS = [
    "Xe bus nào đến thành phố Huế lúc 20:00HR ?",
    "Thời gian xe bus B3 từ Đà Nẵng đến Huế ?",
    "Xe bus nào đến thành phố Hồ Chí Minh ?",
    "Xe bus nào đến thành phố Hồ Chí Minh lúc 20:00HR ?",
    "Xe bus B3 từ Đà Nẵng lúc 2030HR đến thành phố nào ?",
    "Xe bus B3 từ Đà Nẵng đến Huế lúc nào ?"
]

REDUNDANT_TOKENS = [".", ",", "?", ":"]

PATH_TO_OUTPUT = join(".", "Output")
PATH_TO_OUTPUT_FILES = {
    "a": join(PATH_TO_OUTPUT, "output_a.txt"),
    "b": join(PATH_TO_OUTPUT, "output_b.txt"),
    "c": join(PATH_TO_OUTPUT, "output_c.txt"),
    "d": join(PATH_TO_OUTPUT, "output_d.txt"),
    "e": join(PATH_TO_OUTPUT, "output_e.txt"),
    "f": join(PATH_TO_OUTPUT, "output_f.txt"),
}

my_lexicals = {
    "bus": ["bus", "buýt", "xe_bus", "xe_buýt", "xe"],
    "city": ["thành_phố", "tỉnh"],
    "arrive": ["đến", "tới"],
    "from": ["từ"],
    "wh": ["nào"],
    "whtime": ["lúc_nào"],
    "atime": ["lúc", "vào_lúc"],
    "dtime": ["lúc", "từ_lúc"],
    "runtime": ["thời_gian"],
    "busname": ["B1", "B2", "B3", "B4", "B5", "B6"],
    "cityname": ["hue", "hcm", "hn", "danang", "hồ_chí_minh", "hà_nội", "huế", "đà_nẵng"],
    "time": ["time"]
}

# dependency from left --> right
dependency_relations = {
    "PRED": [("<ROOT>", "arrive")],
    "LSUBJ": [("arrive", "bus")],
    "PREP": [("arrive", "from")],
    "FROM-TIME": [
        ("from", "time"),
        ("dtime", "time")],
    "TO-TIME": [("atime", "time")],
    "PREP-TIME": [("arrive", "atime")],
    "FROM-LOC": [("from", "city"), ("from", "cityname")],
    "TO-LOC": [("arrive", "city"), ("arrive", "cityname")],
    "CITY": [("city", "cityname")],
    "BUS-NAME": [("bus", "busname")],
    "WH-BUS": [("bus", "wh")],
    "WH-RUN-TIME": [
        ("arrive", "runtime"),
        ("runtime", "wh")],
    "WH-TIME": [("arrive", "whtime")],
    # "WH-FROM-TIME": [("dtime", "wh"), ("arrive", "wh")],
    # "WH-TO-TIME": [("atime", "wh")],
    "WH-CITY": [("city", "wh")],
}
