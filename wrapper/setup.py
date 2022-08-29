
VERSION = "SIMU.0.0"
ROOT_PATH = "massa"
NODE_SETTINGS_PATH = f'{ROOT_PATH}/massa-models/src/config/constants.rs'

with open(NODE_SETTINGS_PATH, 'r') as f:
    content = f.read()

start_index = content.find("pub static ref VERSION")
end_index = start_index + content[start_index:].find(";")
insertion = "pub static ref VERSION: Version = \"" + VERSION + "\".parse().unwrap();"
content = content[:start_index] + insertion + content[(end_index+1):]
    
start_index = content.find("pub static ref END_TIMESTAMP")
end_index = start_index + content[start_index:].find(";")
insertion = "pub static ref END_TIMESTAMP: Option<MassaTime> = None;"
content = content[:start_index] + insertion + content[(end_index+1):]

with open(NODE_SETTINGS_PATH, 'w') as f:
    content = f.write(content)