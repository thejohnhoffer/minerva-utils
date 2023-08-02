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
    parser.add_argument("exhibit", type=str, help="Path to exhibit.json")
    parser.add_argument("markers", type=str, help="Path to markers.csv")
    args = parser.parse_args()

    # Load JSON data
    exhibit = load_json(args.exhibit)
    marker_list = load_csv(args.markers)

    # To channel Name - ID map
    channel_id_map = {}
    for channel in exhibit['Channels']:
        str_id = channel['Path'].split('_')[1]
        if not str_id.isnumeric(): continue
        channel_id_map[channel['Name']] = int(str_id) 
        channel["Name"] = marker_list[int(str_id)]

    for group in exhibit['Groups']:
        channels = group['Channels']
        for idx in range(len(channels)):
            int_id = channel_id_map[channels[idx]]
            channels[idx] = marker_list[int_id]

    print(json.dumps(exhibit))
