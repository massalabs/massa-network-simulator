## Comment or uncomment git line to use a gitcloned version of massa.

FROM rustlang/rust:nightly

RUN apt-get install -y iproute2
RUN apt-get install -y git
RUN apt-get update
RUN apt-get install -y libclang-11-dev
RUN apt-get install -y build-essential
RUN apt-get install -y python3-pip
RUN pip3 install toml


RUN apt install -y linux-perf
RUN wget https://github.com/jonhoo/inferno/archive/refs/heads/master.zip
RUN unzip master.zip
RUN cd inferno-main/ && cargo build

#RUN mkdir -p /massa/target/release
#RUN mkdir -p /massa/massa-node/

#COPY ./massa/target/release/massa-node /massa/target/release
#COPY ./massa/massa-node /massa/massa-node
COPY ./setup.py /setup.py

ARG GIT_URL=https://github.com/massalabs/massa.git
ARG GIT_BRANCH=main

# clone the repo
RUN git clone "$GIT_URL" -b $GIT_BRANCH massa

RUN python3 /setup.py

RUN cd massa/massa-node && cargo build --release --features sandbox

COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

RUN chmod +x /massa/target/release/massa-node

COPY ./run.sh /massa/run.sh
RUN chmod +x /massa/run.sh

COPY ./config.py /config.py

RUN echo "[]" > /massa/massa-node/base_config/initial_peers.json
RUN echo "" > /massa/massa-node/base_config/initial_ledger.json
RUN echo "" > /massa/massa-node/base_config/initial_rolls.json
RUN apt install -y net-tools

ENTRYPOINT ["/entrypoint.sh"]

