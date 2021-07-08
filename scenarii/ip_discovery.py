from copy import deepcopy
import toml
import json
import time
import re


def ip_discovery_scenario(image, network, config_template, container_wrapper):
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

    container1.start()
    container2.start()

    time.sleep(10)

    log1 = container1.get_logs()
    log2 = container2.get_logs()

    peers_set1 = get_peer_set(log1)
    peers_set2 = get_peer_set(log2)

    expected_set = {ip1, ip2, "169.202.0.10", "169.202.0.11", "169.202.0.12", "169.202.0.13"}
    if peers_set1 != expected_set or peers_set2 != expected_set:
        raise ValueError


# return the set ok known peers
def get_peer_set(log_list):
    peer_set = set()
    for log_elt in log_list:
        for peer in parse_peer_list(log_elt):
            peer_set.add(peer)
    return peer_set


# return ip list
def parse_peer_list(log_string):
    # noinspection PyBroadException
    try:
        regex = r"(?<=DEBUG - node_id=.{50} sent us a peer list: ).*"
        res = list(re.finditer(regex, log_string))[0].group(0)
        return res[1:-1].split(", ")
    except Exception as _e:
        return []
