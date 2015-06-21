__author__ = 'myho'

# https://realpython.com/blog/python/twitter-sentiment-python-docker-elasticsearch-kibana/
# https://github.com/shafiab/HashtagCashtag/blob/master/Kafka/twitterProducer/twitterAPI.py

import json

from kafka import *

from twython import TwythonStreamer

from config import *
from clusterConfig import *


# kafka setup
producer = SimpleProducer(kafka)
topicName = "twitterStream"


class TweetStreamListener(TwythonStreamer):
    def on_success(self, data):
        if 'text' in data:
            producer.send_messages(topicName, json.dumps(data))

    def on_error(self, status_code, data):
        print '!!! error occurred !!!'
        print self
        print data
        print status_code


if __name__ == '__main__':
    stream = TweetStreamListener(consumer_key, consumer_secret, access_key, access_secret)
