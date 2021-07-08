import docker


class NetworkSimulator:
    def __init__(self):
        self.docker_client = docker.from_env()
        self.docker_low_level_client = docker.APIClient()
        self.images = []
        self.containers = []

    def build_wrapper_image(self, wrapper_path):
        print("building wrapper image...")
        image, build_logs = self.docker_client.images.build(path=wrapper_path, rm=True)
        for log_entry in build_logs:
            print("\t{}".format(log_entry))
        self.images.append(image)
        print("wrapper image build process finished")
        return image

    def launch_instance(self, image, dl_kbps, dl_ms, ul_kbps, ul_ms, cmd):
        print("launching instance...")
        container = self.docker_client.containers.run(
            image,
            command=[str(dl_kbps), str(dl_ms), str(ul_kbps), str(ul_ms)] + list(cmd),
            cap_add=["NET_ADMIN"],
            detach=True
        )
        ip = self.docker_low_level_client.inspect_container(container.id).get("NetworkSettings", {}).get("IPAddress")
        self.containers.append(container)
        print("instance launch process finished")
        return container, ip

    def cleanup(self):
        print("cleaning up...")
        while self.containers:
            self.containers.pop().remove(force=True)
        while self.images:
            self.docker_client.images.remove(self.images.pop().id)
        print("cleanup process finished")
