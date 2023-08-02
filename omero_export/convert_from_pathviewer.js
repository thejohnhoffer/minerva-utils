const fs = require('fs');

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
const input_ids = process.argv.slice(2).map(x => x.replace('.json', ''));

if (input_ids.length < 1) {
  console.log('Usage: node convert_from_pathviewer.js $IMAGE_ID1 $IMAGE_ID2...');
  process.exit(1);
}

const template_file = "template.story.json"
const template = read_json(template_file)

for (in_id of input_ids) {
  const groups = [];
  const temp = {...template}
  const path = to_json_path(in_id);
  const input = read_json(path);
  for (group of input.groups) {
    const name = group.name;
    const settings = group.channelSettings;
    const channels = Object.entries(settings).map(([idk, g]) => {
      const color = g.color.replace('#','');
      const min = g.window.start/65535;
      const max = g.window.end/65535;
      const label = `${name} ${idk}`;
      const id = parseInt(idk);
      const info  = ''
      return ({
        label, id, color, min, max, info
      })
    });
    groups.push({
      channels,
      label: name,
      render: channels
    })
  }
  const new_path = `${in_id}.story.json`;
  temp.sample_info.name = in_id;
  temp.groups = groups
  write_json(new_path, temp)
}
