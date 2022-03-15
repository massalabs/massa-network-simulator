from docker_wrapper import DockerWrapper as ContainerWrapper
import gc
from scenarios.ip_discovery import ip_discovery_scenario
from scenarios.banned_peer_try_connection import banned_peer_try_connection
import json
import time

def main():
    print("Initializing...")
    container_wrapper = ContainerWrapper()
    image = container_wrapper.create_image("./wrapper/")
    network = container_wrapper.create_network(
        subnet="169.202.0.0/16",
        gateway_ip="169.202.0.254"
    )

    print("Running network...")
    results = dict()
    n_run, n_success = 0, 0
    with open("nodes.json") as jsonFile:
        nodes_data = json.load(jsonFile)
    for node_data in nodes_data:
        nodes_data_str = json.dumps(nodes_data).encode("utf-8")
        container = container_wrapper.create_container(
            image=image,
            files_dict={
                #"/nodes.json": nodes_data_str,
                "/massa/massa-node/config/node_privkey.key": (node_data["node_privkey"]).encode("utf-8"),
                "/massa/massa-node/config/staking_keys.json": ('["' + node_data["staking_privkey"] + '"]').encode("utf-8")
            },
            network=network,
            ul_kbitps=100,
            ul_ms=100,
            ip=node_data["ip"],
            cmd=["/massa/run.sh"]
        )
        container.start()
        node_data["ip"] = container
    time.sleep(1000)
    print("Cleanup...")
    container_wrapper.delete_containers()
    network.delete()
    image.delete()
    del network
    del image
    del container_wrapper
    gc.collect()

    print("Finished:", n_success, "/", n_run, "tests succeeded")
    exit((0 if n_success == n_run else 1))


if __name__ == "__main__":
    main()
