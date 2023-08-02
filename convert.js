const fs = require('fs');

// Read a json file
const read_json = (path) => {
  return JSON.parse(fs.readFileSync(path, 'utf8'));
}

// function to write a json file to path
const write_json = (path, data) => {
  fs.writeFileSync(path, JSON.stringify(data, null, 2));
}

const input_files = [ "LSP16165.json", "LSP16169.json", "LSP16171.json", "LSP16179.json" ]
const template_file = "template.story.json"


const template = read_json(template_file)
const inputs = input_files.map(i => read_json(i))

for (path of input_files) {
  const groups = [];
  const temp = {...template}
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
  const sample_name = path.split('.').reverse()[1] || '';
  const new_path = `${sample_name}.story.json`;
  temp.sample_info.name = sample_name;
  temp.groups = groups
  write_json(new_path, temp)
}
