#!/bin/bash

cd ../massa-network && \
    cargo build --target x86_64-unknown-linux-musl && \
    cp target/x86_64-unknown-linux-musl/debug/massa_network ../network-simulator/wrapper/massa_network && \
    cd - && \
    python3.7 main.py

