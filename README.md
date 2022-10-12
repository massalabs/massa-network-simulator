# Network Simulator

Use Docker to simulate a P2P network. You can simulate the Massa network on your local network and customize multiple variables :

### 1. [Installation](#installation)
### 2. [Configuration](#configuration)
#### 2.1 [Environnement variable configuration](#environnement-variables)
#### 2.2 [Nodes configuration](#nodes-configuration)
### 3. [Charge network](#charge-network)
### 4. [Monitoring network](#monitoring-network)
----

## Installation

Need docker, git and python3.

Setup:

````
python3 -m venv venv
venv/bin/python -m pip install -r requirements.txt
````

Edit wrapper/Dockerfile and change the following lines:
* ARG GIT_BRANCH="main" # change with the branch you'd like to test

Build docker image :
```
cd wrapper && docker build -t massa-simulator .
```

Launch the simulator :
```
venv/bin/python main.py
```

### Podman

In order to use Podman (~ rootless Docker):

`
sudo apt install podman podman-docker
`

Edit the following file:
* `/etc/containers/registries.conf`
* Add the following line (at the end):
  * `unqualified-search-registries = ["docker.io"]`

Test installation:
* `docker -v`
  * `Emulate Docker CLI using podman. Create /etc/containers/nodocker to quiet msg.
     podman version 3.4.4`

In order to laucnh the simulator, you can have to define the DOCKER_HOST env var:
* `DOCKER_HOST=unix:///run/user/1000/podman/podman.sock venv/bin/python3 main.py`

or better:

* `DOCKER_HOST=unix://$XDG_RUNTIME_DIR/podman/podman.sock venv/bin/python3 main.py`

----
## Configuration
### Environnement variables
The nodes takes environment variable to configure some constants take will modify the network. Currently they are only editable in the `main.py` directly but they will be fetched in your env directly in a next update.

| Variable| Explanation | Default |
|---|---|---|
|GENESIS_TIMESTAMP| Used to setup the genesis_timestamp of the network so that all nodes start on the same network | 30 sec after the launch | 
|T0| Used to define the time between each block | Default value in massa (will be specified here later) |

### Nodes configuration

The nodes need some values to be configured: if they stake, the initial ledger etc. You can find and edit this file in `config/nodes.json`. Here is a explanation of each fields :
```json
{
        "ip": "169.202.0.2", // Ip of the node in the sub network
        "node_privkey": "JqsRffwf4MEsjUKFv2vn2kXGVEr2Jcuit3ooMEkjyh6ZW7yzg", // Private key of the node
        "node_pubkey": "5Zk6UFsghwqjaGRMG6abZjkoGjoZ5bU1H91UWeVqpU7XwjVcEo", // Public key of the node
        "staking_privkey": "JqsRffwf4MEsjUKFv2vn2kXGVEr2Jcuit3ooMEkjyh6ZW7yzg", // Staking key of the node (could be the same as private key)
        "address": "2KziQHMiHmmU3juWPvCYQr1hV3ns8NkXaV3WKH6wV3jycD7SVE", // Address of the node
        "initial_rolls": 100, // Number of rolls at start for the address of the node
        "initial_ledger_balance": 250000000, // Number of coins at start for the address of the node
        "initial_sce_ledger_balance": 100000000,
        "port": 33035, // Port to map on your network to make API calls to the node
        "bootstrap_server": true // Is this server a bootstrap server ? (don't change anything for the moment)
}
```

To get your private key/public key and address use the massa client a run `wallet_generate_private_key` and then `wallet_info` and you will get valid credentials.

----
## Charge network

To add charge to the network you can use the script `charge.py` that will create 32 accounts and provide them money to make a load of operations.

`
venv/bin/python TXPS SHIFT 
`

where:
* TXPS: Number of transaction per seconds (send by batch of 100)
* SHIFT: Used for the amount in transactions

---
## Monitoring network

Logs are available in folder `logs/` when running a network. The is one file by node identified by their IP address in the sub network.

---
## Debug

* `docker container ls`
* `docker exec -it massa_node_169_202_0_1 bash`

### Troubleshooting

* `docker network rm -f br0sim`

### Next steps :

- Improve docs
- More customizable variable
- More easily charging
- Prometheus
- In CI