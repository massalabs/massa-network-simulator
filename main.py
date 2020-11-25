from docker_wrapper import DockerWrapper as ContainerWrapper
import time
import toml
import json
from copy import deepcopy


def run():
    print("initializing...")

    container_wrapper = ContainerWrapper()

    image = container_wrapper.build_wrapper_image("./wrapper/")

    network = container_wrapper.create_network(
        subnet="169.202.0.0/16",
        gateway_ip="169.202.0.254"
    )

    config_template = {
        "logging": {
            "level": 4,
        },
        "protocol": {
            "message_timeout": {"secs": 5, "nanos": 0},
            "ask_peer_list_interval": {"secs": 2, "nanos": 0},
            "network": {
                "bind": "0.0.0.0:50000",
                "routable_ip": None,
                "protocol_port": 50000,
                "connect_timeout": {"secs": 5, "nanos": 0},
                "peers_file": "config/peers.json",
                "target_out_connections": 20,
                "max_in_connections": 100,
                "max_in_connections_per_ip": 5,
                "max_out_connnection_attempts": 10,
                "max_idle_peers": 1000,
                "max_banned_peers": 1000,
                "max_advertise_length": 100000,
                "peers_file_dump_interval": {"secs": 30, "nanos": 0}
            }
        }
    }

    ip1 = "169.202.0.2"
    peers1 = [
        {
            "ip": "169.202.0.10",
            "banned": False,
            "bootstrap": False,
            "last_alive": None,
            "last_failure": None,
            "advertised": True
        },
        {
            "ip": "169.202.0.11",
            "banned": False,
            "bootstrap": False,
            "last_alive": None,
            "last_failure": None,
            "advertised": True
        }
    ]
    config1 = deepcopy(config_template)
    config1["protocol"]["network"]["routable_ip"] = ip1

    ip2 = "169.202.0.3"
    peers2 = [
        {
            "ip": ip1,
            "banned": False,
            "bootstrap": False,
            "last_alive": None,
            "last_failure": None,
            "advertised": True
        },
        {
            "ip": "169.202.0.12",
            "banned": False,
            "bootstrap": False,
            "last_alive": None,
            "last_failure": None,
            "advertised": True
        },
        {
            "ip": "169.202.0.13",
            "banned": False,
            "bootstrap": False,
            "last_alive": None,
            "last_failure": None,
            "advertised": True
        }
    ]
    config2 = deepcopy(config_template)
    config2["protocol"]["network"]["routable_ip"] = ip2

    container1 = container_wrapper.create_container(
        image=image,
        files_dict={
            "/massa-network/config/config.toml": toml.dumps(config1).encode("utf-8"),
            "/massa-network/config/peers.json": json.dumps(peers1).encode("utf-8")
        },
        network=network,
        ul_kbitps=100,
        ul_ms=100,
        ip=ip1,
        cmd=["/massa-network/run.sh"]
    )

    container2 = container_wrapper.create_container(
        image=image,
        files_dict={
            "/massa-network/config/config.toml": toml.dumps(config2).encode("utf-8"),
            "/massa-network/config/peers.json": json.dumps(peers2).encode("utf-8")
        },
        network=network,
        ul_kbitps=100,
        ul_ms=100,
        ip=ip2,
        cmd=["/massa-network/run.sh"]
    )

    print("starting...")

    container_wrapper.start_container(container1)
    container_wrapper.start_container(container2)

    print("waiting...")

    time.sleep(10)

    print("========== CONTAINER 1 ==========")
    print("\n".join(container_wrapper.get_logs(container1)))
    print("=================================\n")
    print("========== CONTAINER 2 ==========")
    print("\n".join(container_wrapper.get_logs(container2)))
    print("=================================\n")

    print("cleaning...")

    del container_wrapper
    print("finished")


run()
