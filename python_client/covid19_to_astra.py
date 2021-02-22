import json
import datetime
import urllib.request, json 
import pulsar


from pulsar.schema import *

class Covid19(Record):
    date = String()
    confirmed = Integer()
    deaths = Integer()
    recovered = Integer()
    country = String()

client = pulsar.Client('pulsar://pulsar:6650')
consumer = client.subscribe(topic='covid19',subscription_name='covid19-to-astra3',schema=AvroSchema(Covid19))

# Connect to Astra
import os
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

astra_user = os.environ.get('ASTRA_USER')

cloud_config = {
    'secure_connect_bundle': '/usr/src/app/secure-connect-'+astra_user+'.zip'
}
auth_provider = PlainTextAuthProvider(username=astra_user, password=os.environ.get('ASTRA_PASS'))
# auth_provider = PlainTextAuthProvider(username='zekedean', password='zekedean')
cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
session = cluster.connect()
session = cluster.connect('zekedean')

# Process the data in pulsar
while True:
    msg = consumer.receive()
    try:
        astra_load = msg.value()
        astra_load = [astra_load.date, astra_load.confirmed, astra_load.deaths, astra_load.recovered, astra_load.country]
        print(astra_load)
        session.execute("INSERT INTO covid19 (date, confirmed, deaths, recovered, country ) VALUES (%s,%s,%s,%s,%s)", astra_load)
        #print(msg.value())
        # Acknowledge successful processing of the message
        consumer.acknowledge(msg)
    except:
        # Message failed to be processed
        consumer.negative_acknowledge(msg)


client.close()