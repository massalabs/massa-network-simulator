import json
from unicodedata import name
import toml

ROOT_PATH = "massa"
CONFIG_PATH = f'{ROOT_PATH}/massa-node/base_config/config.toml'
PEERS_PATH = f'{ROOT_PATH}/massa-node/base_config/initial_peers.json'
NODE_INITIAL_LEDGER_PATH = f'{ROOT_PATH}/massa-node/base_config/initial_ledger.json'
NODE_INITIAL_ROLLS_PATH = f'{ROOT_PATH}/massa-node/base_config/initial_rolls.json'
NODE_INITIAL_SCE_LEDGER_PATH = f'{ROOT_PATH}/massa-node/base_config/initial_sce_ledger.json'
NODES_PATH = f'/nodes.json'

if __name__ == "__main__":
    print("setting up node...")
    nodes = json.load(open(NODES_PATH))
    # setup peers
    res_peers = [{
        "advertised": True,
        "banned": False,
        "bootstrap": True,
        "peer_type": "Bootstrap" if p["bootstrap_server"] == True else "Standard",
        "ip": p["ip"],
        "last_alive": None,
        "last_failure": None
    } for p in nodes]
    with open(PEERS_PATH, "w") as json_file:
        json_file.write(json.dumps(res_peers, indent=2))

    # setup config
    config_data = toml.load(CONFIG_PATH)
    config_data["bootstrap"]["bootstrap_list"] = [
        [srv_v["ip"] + ":31245", srv_v["node_pubkey"]]
        for srv_v in nodes if srv_v["bootstrap_server"] is True
    ]
    config_data["bootstrap"]["per_ip_min_interval"] = 1000
    nb_bootstrap_nodes = len([node for node in nodes if node["bootstrap_server"] is True])
    config_data["network"]["peer_types_config"]["Bootstrap"]["target_out_connections"] = nb_bootstrap_nodes - 1
    config_data["network"]["peer_types_config"]["Bootstrap"]["max_out_attempts"] = nb_bootstrap_nodes - 1
    config_data["network"]["peer_types_config"]["Bootstrap"]["max_in_connections"] = nb_bootstrap_nodes - 1
    config_data["logging"]["level"] = 3

    # dump config
    with open(CONFIG_PATH, "w") as toml_file:
        toml.dump(config_data, toml_file)
    
    #init rolls
    initial_rolls = {}
    for node in nodes:
        if node["initial_rolls"] > 0:
            initial_rolls[node["address"]] = node["initial_rolls"]

    with open(NODE_INITIAL_ROLLS_PATH, "w") as rolls_json_file:
        rolls_json_file.write(json.dumps(initial_rolls, indent=4))
    
    #init sce ledger
    initial_sce_ledger = {}
    for node in nodes:
        if node["initial_sce_ledger_balance"] > 0:
            initial_sce_ledger[node["address"]] = str(node["initial_sce_ledger_balance"])

    with open(NODE_INITIAL_SCE_LEDGER_PATH, "w") as initial_sce_ledger_json_file:
        initial_sce_ledger_json_file.write(json.dumps(initial_sce_ledger, indent=4))

    #init sce ledger
    initial_ledger = {}
    for node in nodes:
        if node["initial_ledger_balance"] > 0:
            initial_ledger[node["address"]] = { "balance": str(node["initial_ledger_balance"]) }

    with open(NODE_INITIAL_LEDGER_PATH, "w") as initial_ledger_json_file:
        initial_ledger_json_file.write(json.dumps(initial_ledger, indent=4))
