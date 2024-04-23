#!/bin/bash

apt-get update
apt-get install python3 python3-pip
pip install -e . --break-system-packages
