FROM rustlang/rust:nightly

RUN apt-get install  iproute2
RUN apt-get install git

ARG GIT_URL=https://github.com/massalabs/massa.git

# clone the repo
RUN git clone -b fix_trace "$GIT_URL" massa

# build node
RUN cd massa/massa-node && cargo build --features sandbox

COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

RUN chmod +x /massa/target/debug/massa-node

COPY ./run.sh /massa/run.sh
RUN chmod +x /massa/run.sh

RUN echo "[]" > /massa/massa-node/base_config/initial_peers.json

ENTRYPOINT ["/entrypoint.sh"]

