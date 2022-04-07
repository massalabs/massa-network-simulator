from copy import deepcopy
import toml
import json
import time
from scenarios.trace_parser import MassaTraceParser
import pandas as pd


def block_transmission(image, network, config_template, container_wrapper):
    start = round(time.time_ns() // 1000000) + 5000

    ip1 = "169.202.0.2"
    peers1 = []
    config1 = deepcopy(config_template)
    config1["network"]["routable_ip"] = ip1
    config1["protocol"]["ask_peer_list_interval"]["secs"] = 60
    config1["consensus"]["current_node_index"] = 0
    config1["consensus"]["genesis_timestamp_millis"] = start

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
    config2["protocol"]["ask_peer_list_interval"]["secs"] = 60
    config2["consensus"]["current_node_index"] = 1
    config2["consensus"]["genesis_timestamp_millis"] = start

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
    config3["protocol"]["ask_peer_list_interval"]["secs"] = 60
    config3["consensus"]["current_node_index"] = 2
    config3["consensus"]["genesis_timestamp_millis"] = start

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
    time.sleep(60)
    # print("\n".join(container1.get_logs()))
    # print("================================\n\n")
    # print("\n".join(container2.get_logs()))
    # print("================================\n\n")
    # print("\n".join(container3.get_logs()))

    res = []
    for _ in range(60):
        time.sleep(1)
        for container_i, log_parser in enumerate(log_parsers):
            for log_entry in log_parser.get_trace_logs():
                if "block" in log_entry["parameters"]:
                    block = log_entry["parameters"]["block"]

                    if log_entry["event"] in ["created_block", "received_block_ok", "received_block_ignore"]:
                        line = [
                            log_entry["date"],
                            container_i,
                            log_entry["event"],
                            block["header"]["creator"][:5],
                            block["header"]["parents"][0][:5],
                            block["header"]["parents"][1][:5],
                            block["header"]["slot_number"],
                            block["header"]["thread_number"],
                            block["signature"][:5]
                        ]
                        if "hash" in log_entry["parameters"]:
                            line.append(
                                log_entry["parameters"]["hash"][:5])
                        else:
                            line.append("-")

                        if "source_node_id" in log_entry["parameters"]:
                            line.append(
                                log_entry["parameters"]["source_node_id"][:5])
                        else:
                            line.append("-")
                        res.append(line)

    columns=[
            'Date',
            'Node_number',
            'Event',
            'Creator',
            'Parent_0',
            'Parent_1',
            'Slot_number',
            'Thread_number',
            'Signature',
            'Block_hash',
            'Source_node_id'
        ]
    print(len(res[0]))
    print(len(columns))
    df = pd.DataFrame(res, columns=columns)

    print(df)
    df.to_csv("output.csv")
    return
    #raise ValueError("peers did not agree on the right peer list in time")
