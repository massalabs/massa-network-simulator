from docker_wrapper import DockerWrapper as ContainerWrapper
import time


def run():
    container_wrapper = ContainerWrapper()
    
    image = container_wrapper.build_wrapper_image("./wrapper/")

    network = container_wrapper.create_network(
        subnet="192.168.52.0/24",
        gateway_ip="192.168.52.254"
    )

    container1 = container_wrapper.create_container(
        image=image,
        files_dict={
            "/test.txt": "lol".encode("utf-8")
        },
        network=network,
        ul_kbitps=100,
        ul_ms=100,
        ip="192.168.52.10",
        cmd=["ping", "192.168.52.11"]
    )

    container2 = container_wrapper.create_container(
        image=image,
        files_dict={
            "/test.txt": "lol".encode("utf-8")
        },
        network=network,
        ul_kbitps=100,
        ul_ms=100,
        ip="192.168.52.11",
        cmd=["ping", "192.168.52.10"]
    )

    container_wrapper.start_container(container1)
    container_wrapper.start_container(container2)

    time.sleep(3)

    print("\n".join(container_wrapper.get_logs(container1)))
    print("\n".join(container_wrapper.get_logs(container2)))


run()
