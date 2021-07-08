FROM rustlang/rust:nightly-alpine

RUN apk add --no-cache iproute2

COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY ./massa_network /massa-network/massa_network
RUN chmod +x /massa-network/massa_network

RUN mkdir /massa-network/config

COPY ./run.sh /massa-network/run.sh
RUN chmod +x /massa-network/run.sh

ENTRYPOINT ["/entrypoint.sh"]

