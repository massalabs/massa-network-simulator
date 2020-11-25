FROM rustlang/rust:nightly-alpine

RUN apk add --no-cache iproute2

COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY ./testnet /massa-network/testnet
RUN chmod +x /massa-network/testnet

RUN mkdir /massa-network/config

COPY ./run.sh /massa-network/run.sh
RUN chmod +x /massa-network/run.sh

ENTRYPOINT ["/entrypoint.sh"]

