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
kafka_client = KafkaClient(kafka_cluster)
producer = SimpleProducer(kafka_client)
topicName = "tweets"

class TweetStreamListener(TwythonStreamer):
    def on_success(self, data):
        print "+++++++++++sending msg+++++++++++++++"
        producer.send_messages(topicName, json.dumps(data))

    def on_error(self, status_code, data):
        print '!!! error occurred !!!'
        print self
        print data
        print status_code


if __name__ == '__main__':
    stream = TweetStreamListener(consumer_key, consumer_secret, access_key, access_secret)

    # only include tweets in SF
    bound = '-118.9448, 32.8007, -117.6462, 34.8233'
    while True:
        try:
            stream.statuses.filter(locations=bound)
        except Exception as e:
            print "++++++++++CRASH+++++++++++"
            print e
            continue