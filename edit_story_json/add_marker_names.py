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

# Function to load CSV data
def load_csv_iter(path):
    with open(path) as f:
        for row in csv.reader(f):
            yield row[0] # Marker Name

load_csv = lambda path: list(load_csv_iter(path))


if __name__ == '__main__':
    # Parse first two command line arguments as pathnames
    parser = argparse.ArgumentParser()
    parser.add_argument("story", type=str, help="Path to story.json")
    parser.add_argument("markers", type=str, help="Path to markers.csv")
    args = parser.parse_args()

    # Load JSON data
    story = load_json(args.story)
    marker_list = load_csv(args.markers)

    # To channel Name - ID map
    for group in story['groups']:
        channels = group['channels']
        for idx in range(len(channels)):
            int_id = int(channels[idx]["id"])
            if int_id >= len(marker_list):
                continue
            old_label = channels[idx]["label"]
            channels[idx]["label"] = marker_list[int_id] 

    print(json.dumps(story))
