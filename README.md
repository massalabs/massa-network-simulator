# Network Simulator

Use Docker to simulate a P2P network

Dependencies: 
```sh
sudo apt install python3 build-essential musl-tools
rustup target add x86_64-unknown-linux-musl --toolchain=nightly
pip3 install docker toml
```

How to use:

* ensure that the network-simulator project folder lies alongside the massa-network one in the same path
* call ./run.sh