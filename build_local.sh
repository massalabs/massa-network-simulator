#!/bin/bash

cd wrapper && mkdir -p massa/target/release && mkdir -p massa/massa-node/ && cp -r ../../massa/target/release/massa-node massa/target/release/ && cp -r ../../massa/massa-node/* massa/massa-node/ && docker build -t massa-simulator .

