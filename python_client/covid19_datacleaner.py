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


with urllib.request.urlopen("https://pomber.github.io/covid19/timeseries.json") as url:
    covid = json.loads(url.read().decode())


client = pulsar.Client('pulsar://pulsar:6650')

producer = client.create_producer(topic='covid19',schema=AvroSchema(Covid19))

# for i in range(10):
#     producer.send(('Hello-%d' % i).encode('utf-8'))




#if you want to run outside of docker, simply change bootstrap_servers="localhost:29092"

# Here we connect to the kafka cluster and grab just one record, all covid data is a giant data dump, we are converting into a stream
# we will also be producing our records
#producer = KafkaProducer(bootstrap_servers="kafka:9092", key_serializer=str.encode,value_serializer=lambda v: json.dumps(v).encode('utf-8'))

count=0
for key in covid:
    print("Processing all entries for -> "+ key)
    for i in covid[key]:

        # we need to ensure our data format is correct to merge the data streams
        # i.e. -> “date”:“2020-01-02" != “date”:“2020-1-2",
        record_date = datetime.datetime.strptime(i['date'], '%Y-%m-%d')
        record_date = record_date.strftime('%Y-%m-%d')
        i['date'] = record_date
        i['country'] = key

        #we are sending our records to a new topic called covid19US
        record = Covid19(date=i['date'],country=i['country'],confirmed=i['confirmed'],deaths=i['deaths'],recovered=i['recovered'] )
        producer.send( partition_key=record_date, content=record ) 
        count+=1

print( str(count) + " Covid19 Records Loaded into Apache Pulsar!")
client.close()