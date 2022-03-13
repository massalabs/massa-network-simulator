import copy
import json
import os
import sys
import time
import toml
import subprocess
import re
import time


COMMIT = "XXXXXXXXXXXXXX"

VERSION = "SIMULATION.0.0"
ROOT_PATH = "massa"
CONFIG_PATH = f'{ROOT_PATH}/massa-node/base_config/config.toml'
PEERS_PATH = f'{ROOT_PATH}/massa-node/base_config/initial_peers.json'
WALLET_PATH = f'{ROOT_PATH}/massa-client/wallet.dat'
STAKING_KEYS_PATH = f'{ROOT_PATH}/massa-node/config/staking_keys.json'
NODE_PRIVKEY_PATH = f'{ROOT_PATH}/massa-node/config/node_privkey.key'
NODE_SETTINGS_PATH = f'{ROOT_PATH}/massa-models/src/node_configuration/default.rs'
NODE_INITIAL_LEDGER_PATH = f'{ROOT_PATH}/massa-node/base_config/initial_ledger.json'
NODE_INITIAL_ROLLS_PATH = f'{ROOT_PATH}/massa-node/base_config/initial_rolls.json'
NODE_INITIAL_SCE_LEDGER_PATH = f'{ROOT_PATH}/massa-node/base_config/initial_sce_ledger.json'


servers = {
   "labnet0": {
       "ip": "XXXXXXXXXXXXXX",
       "node_privkey": "XXXXXXXXXXXXXX",
       "node_pubkey": "XXXXXXXXXXXXXX",
       "staking_privkey": "XXXXXXXXXXXXXX",
       "bootstrap_server": True
   },
   "labnet1": {
       "ip": "XXXXXXXXXXXXXX",
       "node_privkey": "XXXXXXXXXXXXXX",
       "node_pubkey": "XXXXXXXXXXXXXX",
       "staking_privkey": "XXXXXXXXXXXXXX",
       "bootstrap_server": True
   },
}


def run_cmd(cmd, ignore_err=False):
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    process.communicate()
    if process.returncode != 0 and ignore_err == False:
        raise Exception("process failed")
        


if __name__ == "__main__":
    print("setting up simulation...")
    
    # setup peers
    res_peers = [{
        "advertised": True,
        "banned": False,
        "bootstrap": True,
        "ip": p["ip"],
        "last_alive": None,
        "last_failure": None
    } for p in servers.values()]
    with open(PEERS_PATH, "w") as json_file:
        json_file.write(json.dumps(res_peers, indent=2))
    
    # setup version
    with open(NODE_SETTINGS_PATH, 'r') as f:
        content = f.read()
    start_marker = 'pub static ref VERSION: Version = "'
    start_index = content.find(start_marker) + len(start_marker)
    end_index = start_index + content[start_index:].find('"')
    content = content[0:start_index] + VERSION + content[end_index:]
    with open(NODE_SETTINGS_PATH, 'w') as f:
        content = f.write(content)
    
    # setup timestamps
    genesis_timestamp = round(time.time() * 1000) + 60000 * 5  # 5 minutes from now
    
    with open(NODE_SETTINGS_PATH, 'r') as f:
        content = f.read()
    
    start_index = content.find("pub static ref GENESIS_TIMESTAMP")
    end_index = start_index + content[start_index:].find(";")
    insertion = "pub static ref GENESIS_TIMESTAMP: MassaTime = " + str(genesis_timestamp) + ".into();"
    content = content[:start_index] + insertion + content[(end_index+1):]
    
    start_index = content.find("pub static ref END_TIMESTAMP")
    end_index = start_index + content[start_index:].find(";")
    insertion = "pub static ref END_TIMESTAMP: Option<MassaTime> = None;"
    content = content[:start_index] + insertion + content[(end_index+1):]
    
    with open(NODE_SETTINGS_PATH, 'w') as f:
        content = f.write(content)
    
    # setup config
    config_data = toml.load(CONFIG_PATH)
    
    config_data["bootstrap"]["bootstrap_list"] = [
        [srv_v["ip"] + ":31245", srv_v["node_pubkey"]]
        for (srv_n, srv_v) in servers.items() if srv_v["bootstrap_server"] is True
    ]
    config_data["bootstrap"]["per_ip_min_interval"] = 1000
    
    # dump config
    with open(CONFIG_PATH, "w") as toml_file:
        toml.dump(config_data, toml_file)
    
    # setup initial states
    run_cmd("cp ./initial_ledger.json " + NODE_INITIAL_LEDGER_PATH)
    run_cmd("cp ./initial_sce_ledger.json " + NODE_INITIAL_SCE_LEDGER_PATH)
    run_cmd("cp ./initial_rolls.json " + NODE_INITIAL_ROLLS_PATH)
    
    # remove git stuff
    run_cmd("rm -rf massa/.git")
    
    # run script
    with open("massa/massa-node/launch.sh", "w") as outf:
        outf.write("nohup cargo run --release > logs.txt 2>&1 &\n")
    
    # deploy servers

    for srv_name, srv in servers.items():
        print("distributing to", srv_name, "...")

        # setup node staking keys
        res_staking_keys = [srv["staking_privkey"], ]
        with open(STAKING_KEYS_PATH, "w") as json_file:
            json_file.write(json.dumps(res_staking_keys, indent=2))

        # setup node privkey
        with open(NODE_PRIVKEY_PATH, "w") as outf:
            outf.write(srv["node_privkey"])

        # setup node wallet
        res_wallet = [srv["staking_privkey"]]
        with open(WALLET_PATH, "w") as json_file:
            json_file.write(json.dumps(res_wallet, indent=2))

        # setup config
        cfg = copy.deepcopy(config_data)
        # connect to all bootstrap srvs
        cfg["network"]["target_bootstrap_connections"] = len(servers) - 1
        # connect to 3 peers
        cfg["network"]["target_out_nonbootstrap_connections"] = 3
        # allow 10 people in
        cfg["network"]["max_in_nonbootstrap_connections"] = 10
        cfg["network"]["routable_ip"] = srv["ip"]
        cfg["logging"]["level"] = 2

        cfg["bootstrap"]["bootstrap_list"] = [
            [srv_v["ip"] + ":31245", srv_v["node_pubkey"]]
            for (srv_n, srv_v) in servers.items() if srv_v["bootstrap_server"] is True and srv_n != srv_name
        ]
        if srv["bootstrap_server"] is False:
            del cfg["bootstrap"]["bind"]

        with open(CONFIG_PATH, "w") as toml_file:
            toml.dump(cfg, toml_file)

        # release channels (based on build flavors)
        cargo_options = "--release"
        if "--beta" in sys.argv:
            cargo_options += " --features beta"
    print("done 🎉")

