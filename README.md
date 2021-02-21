# Cassandra - Pulsar Example

## Step 1: Make sure you have docker installed and running on your machine!

## Step 2: Create the network

```
docker network create -d bridge pulsar-demo
```

## Step 3: Turn on pulsar (may take a long time) (2GB!)

```
docker run --rm --network pulsar-demo -d -p 6650:6650 -p 8080:8080 --name pulsar apachepulsar/pulsar-standalone
```

### Validate that it is running!

Wait until pulsar gives you the OK status

```
docker logs pulsar | grep "messaging service is ready" 
```

You should get something like the below in the logs 

*23:26:24.517 [main] INFO  org.apache.pulsar.broker.PulsarService - messaging service is ready*

## Step 4: Load the Covid19 data into Pulsar

```
docker run  -ti --network pulsar-demo -v `pwd`:/usr/src/app   apachepulsar/pulsar  python3.7 /usr/src/app/covid19_datacleaner.py
```