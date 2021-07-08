from copy import deepcopy
import toml
import json
import time
from scenarios.trace_parser import MassaTraceParser


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
    config1["network"]["routable_ip"] = ip1

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
    config2["network"]["routable_ip"] = ip2

    ip3 = "169.202.0.4"
    peers3 = [
        {
            "ip": ip2,
            "banned": False,
            "bootstrap": False,
            "last_alive": None,
            "last_failure": None,
            "advertised": True
        },
        {
            "ip": "169.202.0.14",
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
    config3 = deepcopy(config_template)
    config3["network"]["routable_ip"] = ip3

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

    container3 = container_wrapper.create_container(
        image=image,
        files_dict={
            "/massa-network/config/config.toml": toml.dumps(config3).encode("utf-8"),
            "/massa-network/config/peers.json": json.dumps(peers3).encode("utf-8")
        },
        network=network,
        ul_kbitps=100,
        ul_ms=100,
        ip=ip3,
        cmd=["/massa-network/run.sh"]
    )

    container1.start()
    container2.start()
    container3.start()

    expected_peer_set = {ip1, ip2, ip3, "169.202.0.10", "169.202.0.11",
                         "169.202.0.12", "169.202.0.13", "169.202.0.14"}

    log_parsers = [
        MassaTraceParser(container1.get_logs),
        MassaTraceParser(container2.get_logs),
        MassaTraceParser(container3.get_logs)
    ]
    peer_sets = [set(), set(), set()]
    for _ in range(10):
        time.sleep(1)
        for container_i, log_parser in enumerate(log_parsers):
            for log_entry in log_parser.get_trace_logs():
                if log_entry.get("event") == "merge_incoming_peer_list":
                    peer_sets[container_i] = set(log_entry["parameters"]["ips"])
        if all([peer_set == expected_peer_set for peer_set in peer_sets]):
            return

    raise ValueError("peers did not agree on the right peer list in time")
