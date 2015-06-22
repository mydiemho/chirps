#!/usr/bin/python

import sys

from pyelasticsearch.client import ElasticSearch

source = sys.argv[1]

INDEX_NAME = 'twitter'
TYPE = 'tweets'

es = ElasticSearch()

def create_index():
    # create ES client, create index

    mapping = {
        "settings": {
            "number_of_replicas": 2
        },
        "mappings": {
            "tweets": {
                "properties": {
                    "text": {
                        "type": "string"
                    },
                    "location": {
                        "type": "geo_point"
                    },
                    "hashtags": {
                        "type": "string",
                        "index": "not_analyzed"
                    }
                },
                "_ttl": {"enabled": "true", "default": "1h"}
            }

        }
    }

    ## create index
    try:
        es.delete_index(INDEX_NAME)
        print "Index ", INDEX_NAME, " deleted!"
    except Exception as e:
        pass

    res = es.create_index(INDEX_NAME, settings=mapping)
    print "Index ", INDEX_NAME, " created!"
    print res


if __name__ == "__main__":
    create_index()
