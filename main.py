from docker_wrapper import DockerWrapper as ContainerWrapper
import gc
from scenarios.ip_discovery import ip_discovery_scenario
from scenarios.banned_peer_try_connection import banned_peer_try_connection
from scenarios.blocks_transmission import block_transmission
import json
import time
import threading
import cipher

containers = dict()

def logs():
    global containers
    while True:
        for container in containers:
            with open("logs/logs_" + container + ".txt", 'a+') as f:
                f.write('\n'.join(containers[container].get_logs())) 
        time.sleep(2)

def launch_node(container_wrapper, network, genesis_timestamp, nodes_data_str, node_data):
    global containers
    if node_data["launch_time_after_genesis"] and node_data["launch_time_after_genesis"] > 0:
        time.sleep(node_data["launch_time_after_genesis"])
    keypair = {"secret_key": node_data["node_privkey"], "public_key": node_data["node_pubkey"]}
    staking_keys = {node_data["address"]: {"secret_key": node_data["staking_privkey"], "public_key": node_data["node_pubkey"]}}
    container = container_wrapper.create_container(
            files_dict={
                "/nodes.json": nodes_data_str,
                "/massa/massa-node/config/node_privkey.key": json.dumps(keypair).encode("utf-8"),
                "/massa/massa-node/config/staking_wallet.dat": cipher.encrypt(json.dumps(staking_keys))
            },
            name="massa_node_"+node_data["ip"],
            network=network,
            ul_kbitps=1600,
            ul_ms=0,
            ip=node_data["ip"],
            cmd=["/massa/run.sh"],
            environment={
                "GENESIS_TIMESTAMP": str(genesis_timestamp),
            },
            ports={
                33035: node_data["port"]
            }
        )
    container.start()
    containers[node_data["ip"]] = container

def main():
    global containers
    
    container_wrapper = ContainerWrapper()
	
    print("Pruning existing networks and containers...")
    container_wrapper.prune_networks_and_containers()
    
    print("Initializing...")
    network = container_wrapper.create_network(
        subnet="169.202.0.0/16",
        gateway_ip="169.202.0.254"
    )

    print("Running network...")
    n_run, n_success = 0, 0
    with open("config/nodes.json") as jsonFile:
        nodes_data = json.load(jsonFile)
    nodes_data_str = json.dumps(nodes_data).encode("utf-8")
    genesis_timestamp = round(time.time() * 1000) + 10000
    for node_data in nodes_data:
        keypair = {"secret_key": node_data["node_privkey"], "public_key": node_data["node_pubkey"]}
        staking_keys = {node_data["address"]: {"secret_key": node_data["staking_privkey"], "public_key": node_data["node_pubkey"]}}
        if node_data["bootstrap_server"] == True:
            container = container_wrapper.create_container(
                files_dict={
                    "/nodes.json": nodes_data_str,
                    "/massa/massa-node/config/node_privkey.key": json.dumps(keypair).encode("utf-8"),
                    "/massa/massa-node/config/staking_wallet.dat": cipher.encrypt(json.dumps(staking_keys))
                },
                name="massa_node_"+node_data["ip"],
                network=network,
                ul_kbitps=1600,
                ul_ms=0,
                ip=node_data["ip"],
                cmd=["/massa/run.sh"],
                environment={
                    "GENESIS_TIMESTAMP": str(genesis_timestamp),
                },
                ports={
                    33035: node_data["port"]
                }
            )
            container.start()
            containers[node_data["ip"]] = container
        else:
            processThread = threading.Thread(target=launch_node, args=(container_wrapper, network, genesis_timestamp, nodes_data_str, node_data,))
            processThread.start()
    processThread = threading.Thread(target=logs)
    processThread.start()
    input()
    print("Cleanup...")
    container_wrapper.delete_containers()
    network.delete()
    del network
    del container_wrapper
    gc.collect()

    print("Finished:", n_success, "/", n_run, "tests succeeded")
    exit((0 if n_success == n_run else 1))


if __name__ == "__main__":
    main()
