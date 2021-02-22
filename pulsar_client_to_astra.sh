#!/bin/bash

cd /usr/src/app/python_client
pip3.7 install cassandra-driver
python3.7 covid19_to_astra.py