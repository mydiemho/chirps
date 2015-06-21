#!/usr/bin/python

__author__ = 'myho'

# https://realpython.com/blog/python/twitter-sentiment-python-docker-elasticsearch-kibana/
# https://github.com/shafiab/HashtagCashtag/blob/master/Kafka/twitterProducer/twitterAPI.py

import json

from kafka import *

from twython import TwythonStreamer

from config import *
from clusterConfig import *

# kafka setup
kafka_client = KafkaClient(kafka)
producer = SimpleProducer(kafka_client)
topicName = "twitterFilterStream"

class TweetStreamListener(TwythonStreamer):
    def on_success(self, data):
        # look for 'text' to filter ill-formatted tweets in stream
        if 'text' in data and data['coordinates'] != None:
            producer.send_messages(topicName, json.dumps(data))

    def on_error(self, status_code, data):
        print '!!! error occurred !!!'
        print self
        print data
        print status_code


if __name__ == '__main__':
    stream = TweetStreamListener(consumer_key, consumer_secret, access_key, access_secret)

    # only include tweets in sf
    stream.statuses.filter(locations='-122.75,36.8,-121.75,37.8')