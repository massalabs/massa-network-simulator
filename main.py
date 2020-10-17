from simulator import NetworkSimulator
import time

sim = NetworkSimulator()

img = sim.build_wrapper_image("./wrapper/")

container = sim.launch_instance(
    img,
    dl_kbps=100,
    dl_ms=100,
    ul_kbps=100,
    ul_ms=100,
    cmd=["ls", "-a"]
)

print(container)

time.sleep(3)

try:
    logs = container.logs().decode('utf-8')
    print(logs)
except Exception as e:
    pass


sim.cleanup()
