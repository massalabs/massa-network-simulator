#!/bin/sh

python3 config.py && cd /massa/massa-node && RUST_BACKTRACE=full ../target/release/massa-node -p test && sleep 30