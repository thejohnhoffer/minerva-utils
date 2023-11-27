import json
import sys

def from_json(fname, cname):
    with open(fname, "r") as fh:
        data = json.load(fh)
        groups = data['groups']
        for group in groups:
            channels = [r['label'] for r in group['render']]
            # get index of cname in channels
            try:
                idx = channels.index(cname)
                group['channels'] = [group['channels'][idx]]
                group['render'] = [group['render'][idx]]
                data['defaults'] = group['render']
                data['waypoints'] = []
                data['groups'] = [group]
                if 'autosave' in data:
                    del data['autosave']
                return data
            except ValueError:
                continue

if __name__ == "__main__":
    fname = sys.argv[1]
    cname = sys.argv[2]
    best_group  = from_json(fname, cname)
    print(json.dumps(best_group))
