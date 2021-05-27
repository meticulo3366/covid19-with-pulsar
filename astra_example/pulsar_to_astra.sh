#!/bin/bash

bin/pulsar-admin --admin-url http://pulsar:8080 sinks create \
	--name covid19 \
	--classname com.datastax.oss.sink.pulsar.StringCassandraSinkTask \
	--sink-config-file /usr/src/app/pulsar_to_astra.yml \
	--sink-type cassandra-enhanced \
	--tenant public \
	--namespace default \
	--inputs covid19 
	#--inputs "persistent://public/default/covid19"