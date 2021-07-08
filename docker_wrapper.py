import docker
import docker.types
import os
from io import BytesIO
import tarfile
import warnings


class DockerWrapper:
    def __init__(self):
        self.docker_client = docker.from_env()
        self.images = []
        self.networks = []
        self.containers = []

    @staticmethod
    def get_logs(container, from_line=0):
        return container.logs().decode('utf-8').split("\n")[from_line:]

    def build_wrapper_image(self, wrapper_path):
        image, _ = self.docker_client.images.build(path=wrapper_path, rm=True)
        self.images.append(image)
        return image

    def create_network(self, subnet, gateway_ip):
        result = self.docker_client.networks.create(
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
        self.networks.append(result)
        return result

    def create_container(self, image, files_dict, network, ul_kbitps, ul_ms, ip, cmd):
        result = self.docker_client.api.create_container(
            image.id,
            command=[str(ul_kbitps), str(ul_ms)] + list(cmd),
            detach=True,
            host_config=self.docker_client.api.create_host_config(
                cap_add=["NET_ADMIN"]
            ),
            networking_config=self.docker_client.api.create_networking_config({
                network.id: self.docker_client.api.create_endpoint_config(
                    ipv4_address=str(ip),
                )
            })
        )
        warns = result.get("Warnings")
        if warns:
            warnings.warn(warns)
        container = self.docker_client.containers.get(result["Id"])
        self.containers.append(container)
        for file_path, file_bytes in files_dict.items():
            (file_dir, file_name) = os.path.split(file_path)
            archive_buffer = BytesIO()
            archive = tarfile.open(mode="w:", fileobj=archive_buffer)
            file_info = tarfile.TarInfo(file_name)
            file_info.size = len(file_bytes)
            archive.addfile(tarinfo=file_info, fileobj=BytesIO(file_bytes))
            archive.close()
            archive_buffer.seek(0)
            if not container.put_archive(file_dir, archive_buffer.read()):
                raise ValueError("failed adding file {} to container {}".format(file_path, container.id))
        return container

    @staticmethod
    def start_container(container):
        container.start()

    def cleanup(self):
        while self.containers:
            target = self.containers.pop()
            try:
                target.remove(force=True)
            except Exception as e:
                warnings.warn("failed removing container {}: {}".format(target.id, e))
        while self.networks:
            target = self.networks.pop()
            try:
                target.remove()
            except Exception as e:
                warnings.warn("failed removing network {}: {}".format(target.id, e))
        while self.images:
            target = self.images.pop()
            try:
                self.docker_client.images.remove(target.id)
            except Exception as e:
                warnings.warn("failed removing image {}: {}".format(target.id, e))

    def __del__(self):
        self.cleanup()
