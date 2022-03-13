FROM rustlang/rust:nightly

RUN apt-get install  iproute2
RUN apt-get install git

ARG GIT_URL=https://github.com/massalabs/massa.git

# clone the repo
RUN git clone -b fix_trace "$GIT_URL" massa

COPY ./initial_ledger.json /initial_ledger.json
COPY ./initial_rolls.json /initial_rolls.json
COPY ./initial_sce_ledger.json /initial_sce_ledger.json
COPY ./config.py /config.py

RUN apt update
RUN apt-get install -y python3-pip
RUN pip3 install toml

RUN python3 /config.py

# build node
RUN cd massa/massa-node && cargo build --release

COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

RUN chmod +x /massa/target/debug/massa-node

COPY ./run.sh /massa/run.sh
RUN chmod +x /massa/run.sh

RUN echo "[]" > /massa/massa-node/base_config/initial_peers.json

ENTRYPOINT ["/entrypoint.sh"]

