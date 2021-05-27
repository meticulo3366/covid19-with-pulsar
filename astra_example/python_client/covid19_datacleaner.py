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

#parse the covid19 data

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