from docker_wrapper import DockerWrapper as ContainerWrapper
import gc
from scenarios.ip_discovery import ip_discovery_scenario
from scenarios.banned_peer_try_connection import banned_peer_try_connection
import json
import time
import threading

def logs(containers):
    while True:
        for container in containers:
            with open("logs/logs_" + container + ".txt", 'w+') as f:
                f.write('\n'.join(containers[container].get_logs())) 
        time.sleep(2)

def main():
    print("Initializing...")
    container_wrapper = ContainerWrapper()
    network = container_wrapper.create_network(
        subnet="169.202.0.0/16",
        gateway_ip="169.202.0.254"
    )

    print("Running network...")
    n_run, n_success = 0, 0
    with open("config/nodes.json") as jsonFile:
        nodes_data = json.load(jsonFile)
    nodes_data_str = json.dumps(nodes_data).encode("utf-8")
    genesis_timestamp = round(time.time() * 1000) + 30000
    containers = dict()
    for node_data in nodes_data:
        container = container_wrapper.create_container(
            files_dict={
                "/nodes.json": nodes_data_str,
                "/massa/massa-node/config/node_privkey.key": (node_data["node_privkey"]).encode("utf-8"),
                "/massa/massa-node/config/staking_keys.json": ('["' + node_data["staking_privkey"] + '"]').encode("utf-8")
            },
            name="massa_node_"+node_data["ip"],
            network=network,
            ul_kbitps=100,
            ul_ms=100,
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
    processThread = threading.Thread(target=logs, args=(containers,))
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
