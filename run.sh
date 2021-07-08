#!/bin/bash

cd ../massa-network && \
    cargo build --target x86_64-unknown-linux-musl && \
    cp target/x86_64-unknown-linux-musl/debug/testnet ../network-simulator/wrapper/testnet && \
    cd - && \
    python3 main.py

