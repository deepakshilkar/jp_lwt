import zipfile as z
import json
from collections import OrderedDict

epwing = OrderedDict([])

def process_json_dict(path):
    with z.ZipFile(path, "r") as f:
        for name in f.namelist():
            if name != "index.json":
                data = json.loads(f.read(name))
                for entry in data:
                    epwing[entry[0]] = [entry[0], entry[1], entry[5]]
                    epwing[entry[1]] = [entry[0], entry[1], entry[5]]


process_json_dict("reader/epwing.zip")
