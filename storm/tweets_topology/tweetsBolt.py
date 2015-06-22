import json
import logging

from kafka import KafkaClient, SimpleProducer
import pyelasticsearch
from pyleus.storm import SimpleBolt


# GOTCHA:
# have to include "http://" and ends with "/", else will throw error
ELASTIC_SEARCH_CLUSTER = [
    "http://52.8.145.247:9200/", "http://52.8.148.251:9200/", "http://52.8.158.130:9200/", "http://52.8.162.105:9200/",
    "http://52.8.153.92:9200/"]

KAFKA_CLUSTER = "52.8.145.247:9092,52.8.148.251:9092,52.8.158.130:9092,52.8.162.105:9092,52.8.153.92:9092"

log = logging.getLogger("geo_update_topology.geo_update_bolt")

es = pyelasticsearch.ElasticSearch(urls=ELASTIC_SEARCH_CLUSTER)
kafka_client = KafkaClient(hosts=KAFKA_CLUSTER)
producer = SimpleProducer(kafka_client)
index = "twitter"

class TweetsBolt(SimpleBolt):

    def process_tuple(self, tup):
        request = tup.values

        # convert the extract value to a JSON object
        data = json.loads(request[0])
        log.debug("+++++++++++++++++++RECEIVED MSG++++++++++++++++++++")


        # skip retweets
        if data['retweet_count']:
                return True

        # skip if already in couch
        if status.id_str in db:
                return True
        # look for 'text' to filter ill-formatted tweets in stream
        if 'text' in data and data['coordinates'] != None:

            # build object to store in elasticsearch
            coordinates = data['coordinates']['coordinates']
            hashtag_map = data['entities']['hashtags']
            hashtags = []

            # normalize hashtags
            for ob in hashtag_map:
                hashtags.append(ob['text'].lower())

            text = data['text']

            dict = {
                'location': {
                    'lat': coordinates[1],
                    'lon': coordinates[0]
                },
                'text': text
            }

            if len(hashtags) != 0:
                dict['hashtags'] = hashtags

            res = es.index(index=index, doc_type="tweets", doc=dict)
            log.debug(json.dumps(res))
            log.debug("\n")

if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        filename='/tmp/pyleus/tweets_bolt.log',
        format="%(message)s",
        filemode='a'
    )

    TweetsBolt().run()
