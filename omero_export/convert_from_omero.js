const fs = require('fs');

const TEMPLATE = {
  "is_autosave": false,
  "defaults": [],
  "waypoints": [
    {
      "name": "",
      "text": "",
      "pan": [
          0.5,
          0.5
      ],
      "zoom": 1,
      "masks": [],
      "arrows": [],
      "overlays": [],
      "group": "overview"
    }
  ],
  "groups": [],
  "sample_info": {
      "pixels_per_micron": 0,
      "rotation": 0,
      "name": "",
      "text": ""
  },
  "csv_file": "",
  "in_file": "",
  "root_dir": ".",
  "out_name": "",
  "masks": []
}
// Read a json file
const read_json = (path) => {
  if (!fs.existsSync(path)) {
    console.log(`Error: ${path} does not exist`);
    process.exit(1);
  }
  if (!path.endsWith('.json')) {
    console.log(`Error: ${path} is not a json file`);
    process.exit(1);
  }
  return JSON.parse(fs.readFileSync(path, 'utf8'));
}

// function to write a json file to path
const write_json = (path, data) => {
  fs.writeFileSync(path, JSON.stringify(data, null, 2));
}

// function to add .json extension to string
const to_json_path = (path) => {
  return `${path}.json`;
}

// get all user provide arguments
const in_files = process.argv.slice(2);

if (in_files.length != 2) {
  console.log('Usage: node convert_from_omero.js $IN_F $OUT_F');
  process.exit(1);
}

const key_to_id = (key) => {
  return parseInt(key) - 1;
}

const format_channel = ([k, channel]) => {
  const { color, start, end, label } = channel;
  const id = key_to_id(k);
  return {
    color: color.toLowerCase(),
    id, label, info: "",
    min: start / 65535,
    max: end / 65535,
  };
}

const convert = ((in_f, out_f) => {
  const { channels } = read_json(in_f);
  const sources = Object.entries(channels);
  // Format all channels and active channels
  const all_channels = sources.map(format_channel);
  const active_channels = sources.reduce((o, kv) => {
    return kv[1].active ? [...o, format_channel(kv)] : o;
  }, []);

  const result = {
    ...TEMPLATE,
    groups: [{
      label: "overview",
      render: active_channels,
      channels: active_channels
    },
    {
      label: "all channels",
      render: all_channels,
      channels: all_channels
    }]
  }
  write_json(out_f, result);

})(in_files[0], in_files[1])
