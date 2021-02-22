#!/bin/bash

bin/pulsar-admin --admin-url http://pulsar:8080 sinks localrun \
	--name covid19 \
	--archive /usr/src/app/connectors/cassandra-enhanced-pulsar-sink-1.4.0.nar \
	--sink-config-file /usr/src/app/pulsar_to_astra.yml \
	--tenant public \
	--namespace default \
	--inputs covid19 
	#--inputs "persistent://public/default/covid19"