#!/bin/bash

sudo apt-get update
sudo apt-get install python3 python3-pip
pip install -e . --break-system-packages
