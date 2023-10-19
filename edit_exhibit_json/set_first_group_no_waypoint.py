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
    args = parser.parse_args()

    # Load JSON data
    exhibit = load_json(args.exhibit)

    # Set the first group
    grp =  exhibit['Groups'][0]
    exhibit['FirstGroup'] = grp['Name']

    # Remove all waypoints
    exhibit['Stories'][0]['Waypoints'] = []

    print(json.dumps(exhibit))
