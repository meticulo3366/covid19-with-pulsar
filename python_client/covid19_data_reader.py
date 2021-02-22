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
consumer = client.subscribe(topic='covid19',subscription_name='covid19-subscription',schema=AvroSchema(Covid19))

while True:
    msg = consumer.receive()
    try:
        print(msg.value())
        # Acknowledge successful processing of the message
        consumer.acknowledge(msg)
    except:
        # Message failed to be processed
        consumer.negative_acknowledge(msg)

client.close()