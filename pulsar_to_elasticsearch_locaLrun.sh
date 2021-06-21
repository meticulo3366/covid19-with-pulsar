#!/bin/bash

# bin/pulsar-admin --admin-url http://pulsar:8080 sinks localrun --help

bin/pulsar-admin --admin-url http://pulsar:8080 sinks localrun \
    --broker-service-url pulsar://pulsar:6650 \
    --archive /pulsar/connectors/pulsar-io-elastic-search-2.7.2.nar \
    --tenant public \
    --namespace default \
    --name elasticsearch-test-sink \
    --sink-config-file /usr/src/app/elasticsearch-sink.yaml \
	--inputs covid19 