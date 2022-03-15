import json
from unicodedata import name
import toml

ROOT_PATH = "massa"
CONFIG_PATH = f'{ROOT_PATH}/massa-node/base_config/config.toml'
PEERS_PATH = f'{ROOT_PATH}/massa-node/base_config/initial_peers.json'
NODES_PATH = f'/nodes.json'

if __name__ == "__main__":
    print("setting up node...")
    servers = json.load(open(NODES_PATH))
    # setup peers
    res_peers = [{
        "advertised": True,
        "banned": False,
        "bootstrap": True,
        "ip": p["ip"],
        "last_alive": None,
        "last_failure": None
    } for p in servers]
    with open(PEERS_PATH, "w") as json_file:
        json_file.write(json.dumps(res_peers, indent=2))

    # setup config
    config_data = toml.load(CONFIG_PATH)
    config_data["bootstrap"]["bootstrap_list"] = [
        [srv_v["ip"] + ":31245", srv_v["node_pubkey"]]
        for srv_v in servers if srv_v["bootstrap_server"] is True
    ]
    config_data["bootstrap"]["per_ip_min_interval"] = 1000

    # dump config
    with open(CONFIG_PATH, "w") as toml_file:
        toml.dump(config_data, toml_file)
