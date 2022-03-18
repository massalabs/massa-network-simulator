#!/bin/bash

cd wrapper && docker build -t massa-test . && cd .. && python3 main.py

