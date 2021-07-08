from copy import deepcopy
import toml
import json
import time
from scenarii.trace_parser import MassaTraceParser


def block_transmission(image, network, config_template, container_wrapper):
    ip1 = "169.202.0.2"
    peers1 = []
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
        }]
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
        }]
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

    
    
    log_parsers = [
        MassaTraceParser(container1.get_logs),
        MassaTraceParser(container2.get_logs),
        MassaTraceParser(container3.get_logs)
    ]
    print("\n".join(container1.get_logs()))



    raise ValueError("peers did not agree on the right peer list in time")
