from docker_wrapper import DockerWrapper as ContainerWrapper
import gc
from scenarios.ip_discovery import ip_discovery_scenario
from scenarios.banned_peer_try_connection import banned_peer_try_connection


def main():
    print("Initializing...")
    container_wrapper = ContainerWrapper()
    image = container_wrapper.create_image("./wrapper/")
    network = container_wrapper.create_network(
        subnet="169.202.0.0/16",
        gateway_ip="169.202.0.254"
    )

    config_template = {
        "logging": {
            "level": 4,
        },
        "network": {
            "bind": "0.0.0.0:50000",
            "routable_ip": None,
            "protocol_port": 50000,
            "connect_timeout":5000,
            "wakeup_interval": 10000,
            "peers_file": "config/peers.json",
            "target_out_connections": 20,
            "max_in_connections": 100,
            "max_in_connections_per_ip": 5,
            "max_out_connnection_attempts": 10,
            "max_idle_peers": 1000,
            "max_banned_peers": 1000,
            "max_advertise_length": 100000,
            "peers_file_dump_interval": 30000
        },
        "protocol": {
            "message_timeout": 5000,
            "ask_peer_list_interval": 2000
        },
        "consensus":{
            "genesis_timestamp" : 1607958448000,
            "t0" : 16000,
            "thread_count" : 2,
            "selection_rng_seed" :  42,
            "genesis_key" : 'SGoTK5TJ9ZcCgQVmdfma88UdhS6GK94aFEYAsU3F1inFayQ6S',
            "nodes" : [
                ['4vYrPNzUM8PKg2rYPW3ZnXPzy67j9fn5WsGCbnwAnk2Lf7jNHb','LGXe9RrR1QNSsSn8bAEgrsYM8WwX67oHLjGj6e19bCW9ZKo6p'],
                ['6ZoZ46HVJMKVTU92a1QRQqWpERL5tTAJ4RjazPBRzFXLmMDu8g','PZZzhDKrdGiuQMGEazTGP5b164qofYXh9Yp4SQ4uZChxAQqtK'],
                ['54VEbD2R2HkUz2G5NGHyxhaFDhrQFG62UqFLWsUywnHtDsM8qh','2eLQSjhrep9Grw7yDifXnDKgCc1WTXBCtdeREzuJd9jiSZuZmr']
            ],
            "current_node_index" : 0
        }

    }

    print("Running tests...")
    test_functions = {
        "ip_discovery_scenario": ip_discovery_scenario,
        "banned_peer_try_connection": banned_peer_try_connection,
    }
    results = dict()
    n_run, n_success = 0, 0
    for test_name, test_function in test_functions.items():
        n_run += 1
        try:
            test_function(image, network, config_template, container_wrapper)
            results[test_name] = {"ok": True}
            n_success += 1
            print("Test", test_name, "PASSED ヾ(＾-＾)ノ")
        except Exception as e:
            results[test_name] = {"ok": False, "exception": e}
            print("Test", test_name, "FAILED (╯︵╰,) =>", e)
        finally:
            container_wrapper.delete_containers()
            gc.collect()

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
