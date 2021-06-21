#!/bin/bash

# bin/pulsar-admin --admin-url http://pulsar:8080 sinks localrun --help

bin/pulsar-client --url pulsar://pulsar:6650 consume covid19 -n 0 -p Earliest -s test_covid