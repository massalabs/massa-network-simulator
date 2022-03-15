import docker
import docker.types
import os
from io import BytesIO
import tarfile
import warnings
import re


class DockerWrapper:
    def __init__(self):
        self.docker_client = docker.from_env()
        self.containers = []

    def create_network(self, subnet: str, gateway_ip: str):
        return NetworkWrapper(self, subnet, gateway_ip)

    def create_container(self, network, files_dict: dict, ul_kbitps: int, ul_ms: int, ip: str, cmd: list, environment: dict):
        new_container = ContainerWrapper(
            self, network, files_dict, ul_kbitps, ul_ms, ip, cmd, environment)
        self.containers.append(new_container)
        return new_container

    def delete_containers(self):
        for itm in self.containers:
            itm.delete()
        self.containers.clear()


class NetworkWrapper:
    def __init__(self, wrapper: DockerWrapper, subnet: str, gateway_ip: str):
        self.wrapper = wrapper
        self.network = self.wrapper.docker_client.networks.create(
            name="br0sim",
            driver="bridge",
            ipam=docker.types.IPAMConfig(
                pool_configs=[
                    docker.types.IPAMPool(
                        subnet=subnet,
                        gateway=gateway_ip
                    )
                ]
            )
        )
        self.id = self.network.id

    def delete(self):
        if self.network is not None:
            self.network.remove()
            self.network = None

    def __del__(self):
        try:
            self.delete()
        except Exception as e:
            warnings.warn("failed removing network {}: {}".format(self.id, e))


class ContainerWrapper:
    def __init__(self, wrapper: DockerWrapper, network: NetworkWrapper,
                 files_dict: dict, ul_kbitps: int, ul_ms: int, ip: str, cmd: list, environment: dict):

        result = wrapper.docker_client.api.create_container(
            "massa-simulator",
            command=[str(ul_kbitps), str(ul_ms)] + cmd,
            detach=True,
            host_config=wrapper.docker_client.api.create_host_config(
                cap_add=["NET_ADMIN"]
            ),
            networking_config=wrapper.docker_client.api.create_networking_config({
                network.id: wrapper.docker_client.api.create_endpoint_config(
                    ipv4_address=str(ip),
                )
            }),
            environment=environment
        )
        warns = result.get("Warnings")
        if warns:
            warnings.warn(warns)
        self.id = result["Id"]
        self.container = wrapper.docker_client.containers.get(self.id)

        for file_path, file_bytes in files_dict.items():
            (file_dir, file_name) = os.path.split(file_path)
            archive_buffer = BytesIO()
            archive = tarfile.open(mode="w:", fileobj=archive_buffer)
            file_info = tarfile.TarInfo(file_name)
            file_info.size = len(file_bytes)
            archive.addfile(tarinfo=file_info, fileobj=BytesIO(file_bytes))
            archive.close()
            archive_buffer.seek(0)
            if not self.container.put_archive(file_dir, archive_buffer.read()):
                raise ValueError(
                    "failed adding file {} to container {}".format(file_path, self.id))

    def start(self):
        self.container.start()

    def get_logs(self, from_line=0):
        logs = self.container.logs().decode('utf-8').split("\n")[from_line:]
        for log_line in logs:
            log_line = re.sub(r'\x1b\[\d+m', '', log_line)
        return logs

    def delete(self):
        if self.container is not None:
            self.container.remove(force=True)
            self.container = None

    def __del__(self):
        try:
            self.delete()
        except Exception as e:
            warnings.warn(
                "failed removing container {}: {}".format(self.id, e))
