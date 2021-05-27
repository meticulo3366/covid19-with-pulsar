#!/bin/bash

$ bin/pulsar-admin sinks localrun \
    --archive connectors/pulsar-io-elastic-search-2.7.2.nar \
    --tenant public \
    --namespace default \
    --name elasticsearch-test-sink \
    --sink-type elastic_search \
    --sink-config-file elasticsearch-sink.yml \
	--inputs covid19 