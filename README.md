# Cassandra - Pulsar Example

## Step 1: Make sure you have docker installed and running on your machine!

## Step 2: Create the network

```
docker network create -d bridge pulsar-demo
```


## Step 3: [Download DSE pulsar connector and put in this current directory](https://downloads.datastax.com/#apc)

## Step 4: extract contents of the package

```
tar zxf cassandra-enhanced-pulsar-sink.tar.gz
```


## Step 5: Create Connectors folder

```
mkdir connectors
```


## Step 5: Move the contents of the package

```
mv cassandra-enhanced-pulsar-sink-1.4.0/cassandra-enhanced-pulsar-sink-1.4.0.nar connectors/cassandra-enhanced-pulsar-sink-1.4.0.nar
```

## Step 3: Turn on pulsar (may take a long time) (2GB!)

```
docker run -v `pwd`/connectors:/pulsar/connectors --rm --network pulsar-demo -d -p 6650:6650 -p 8080:8080 --name pulsar apachepulsar/pulsar-standalone
```

### Validate that it is running!

Wait until pulsar gives you the OK status

```
docker logs pulsar | grep "messaging service is ready" 
```

You should get something like the below in the logs 

*23:26:24.517 [main] INFO  org.apache.pulsar.broker.PulsarService - messaging service is ready*

## Validate the Cassandra Enhanced Connector is running

```
curl -s http://localhost:8080/admin/v2/functions/connectors
```

You should get output like the below

*[{"name":"cassandra-enhanced","description":"A DataStax Pulsar Sink to load records from Pulsar topics to Apache Cassandra(R) or DataStax Enterprise(DSE)\n","sinkClass":"com.datastax.oss.sink.pulsar.RecordCassandraSinkTask"}]*

## Step 4: Load the Covid19 data into Pulsar

```
docker run  -ti --network pulsar-demo -v `pwd`/python_client:/usr/src/app   apachepulsar/pulsar  python3.7 /usr/src/app/covid19_datacleaner.py
```


## Step 6: Send to Cassandra

```
docker run  -ti --network pulsar-demo -v `pwd`:/usr/src/app   apachepulsar/pulsar /usr/src/app/pulsar_to_astra.sh
```

You should get output like the below

*"Created successfully"*

## Step 6: Display in Cassandra



