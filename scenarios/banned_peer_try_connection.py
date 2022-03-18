from copy import deepcopy
import toml
import json
import time
from scenarios.trace_parser import MassaTraceParser


def banned_peer_try_connection(image, network, config_template, container_wrapper):
    ip1 = "169.202.0.2"
    ip2 = "169.202.0.3"

    peers1 = [
        {
            "ip": ip2,
            "banned": True,
            "bootstrap": False,
            "last_alive": None,
            "last_failure": None,
            "advertised": True
        }
    ]
    config1 = deepcopy(config_template)
    config1["network"]["routable_ip"] = ip1

    peers2 = [
        {
            "ip": ip1,
            "banned": False,
            "bootstrap": False,
            "last_alive": None,
            "last_failure": None,
            "advertised": True
        }
    ]
    config2 = deepcopy(config_template)
    config2["network"]["routable_ip"] = ip2

    container1 = container_wrapper.create_container(
        image=image,
        files_dict={
            "/massa/massa-node/config/config.toml": toml.dumps(config1).encode("utf-8"),
            "/massa/massa-node/config/peers.json": json.dumps(peers1).encode("utf-8")
        },
        network=network,
        ul_kbitps=100,
        ul_ms=100,
        ip=ip1,
        cmd=["/massa/run.sh"]
    )

    container2 = container_wrapper.create_container(
        image=image,
        files_dict={
            "/massa/massa-node/config/config.toml": toml.dumps(config2).encode("utf-8"),
            "/massa/massa-node/config/peers.json": json.dumps(peers2).encode("utf-8")
        },
        network=network,
        ul_kbitps=100,
        ul_ms=100,
        ip=ip2,
        cmd=["/massa/run.sh"]
    )

    container1.start()
    container2.start()

    log_parsers = [
        MassaTraceParser(container1.get_logs),
        MassaTraceParser(container2.get_logs)
    ]
    for _ in range(10):
        time.sleep(1)
        for container_i, log_parser in enumerate(log_parsers):
            for log_entry in log_parser.get_trace_logs():
                if container_i == 0 \
                        and log_entry.get("event") == "in_connection_refused_peer_banned" \
                        and log_entry.get("parameters", {}).get("ip") == ip2:
                    return

    raise ValueError("banned peer connection rejection did not happen in time")
