from docker_wrapper import DockerWrapper as ContainerWrapper
import gc
from scenarii.ip_discovery import ip_discovery_scenario


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
        "protocol": {
            "message_timeout": {"secs": 5, "nanos": 0},
            "ask_peer_list_interval": {"secs": 2, "nanos": 0},
            "network": {
                "bind": "0.0.0.0:50000",
                "routable_ip": None,
                "protocol_port": 50000,
                "connect_timeout": {"secs": 5, "nanos": 0},
                "wakeup_interval": {"secs": 10, "nanos": 0},
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

    print("Running tests...")
    test_functions = {
        "ip_discovery_scenario": ip_discovery_scenario,
        "test_2": ip_discovery_scenario,
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
            print("Test", test_name, "FAILED =>", e)
        finally:
            gc.collect()

    print("Cleanup...")
    del network
    del image
    del container_wrapper
    gc.collect()

    print("Finished:", n_success, "/", n_run, "tests succeeded")
    exit((0 if n_success == n_run else 1))


if __name__ == "__main__":
    main()
