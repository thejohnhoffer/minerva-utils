import argparse
import json
import sys
import csv

# Function to write JSON data
def write_json(path, data):
    print(json.dumps(data, f))

# Function to load JSON data
def load_json(path):
    with open(path) as f:
        return json.load(f)

if __name__ == '__main__':
    # Parse first two command line arguments as pathnames
    parser = argparse.ArgumentParser()
    parser.add_argument("auto", type=str, help="Path to auto.json")
    parser.add_argument("template", type=str, help="Path to template.json")
    args = parser.parse_args()

    # Load JSON data
    auto = load_json(args.auto)
    template = load_json(args.template)
    min_max_map = {}

    # Auto minerva auto
    for group in auto['groups']:
        channels = group['channels']
        for channel in channels:
            _id = channel["id"]
            _min = channel["min"]
            _max = channel["max"]
            label = channel["label"]
            min_max_map[label] = {
                "min": _min, "max": _max, "id": _id
            }

    # To channel Name - ID map
    for group in template['groups']:

        for key in ["channels", "render"]:
            channels = group[key]
            for idx in range(len(channels)):
                label = channels[idx]["label"]
                min_max = min_max_map.get(label, None)
                if min_max == None:
                    continue
                
                channels[idx]["min"] = min_max["min"]
                channels[idx]["max"] = min_max["max"]
                channels[idx]["id"] = min_max["id"]

    print(json.dumps(template))
