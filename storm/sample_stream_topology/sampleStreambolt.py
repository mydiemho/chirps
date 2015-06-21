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


class SampleStreamBolt(SimpleBolt):

    def process_tuple(self, tup):
        request = tup.values

        # convert the extract value to a JSON object
        parsed_msg = json.loads(request[0])

        log.debug("+++++++++++++++++++RECEIVED MSG++++++++++++++++++++")
        log.debug(json.dump(parsed_msg))

        # indexname = 'taxi_index'
        # taxi_type = 'taxi'
        # taxi_id = parsed_msg['taxi_id']
        # taxi_doc = {
        #     "location": {
        #         "lat": parsed_msg['location']['latitude'],
        #         "lon": parsed_msg['location']['longitude']
        #     }
        # }
        #
        # try:
        #     res = es.update(index=indexname,
        #                     id=taxi_id,
        #                     doc=taxi_doc,
        #                     doc_type=taxi_type,
        #                     retry_on_conflict=2)
        #
        #     log.debug("+++++++++++++++++++updated location for taxi %s++++++++++++++++++++", taxi_id)
        #     log.debug("%s\n", res)
        # except Exception as e:
        #     log.error("++++++++++FAILED TO UPDATE GEO+++++++++")
        #     log.error("%s\n", str(e))


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        filename='/tmp/pyleus/sample_stream_bolt.log',
        format="%(message)s",
        filemode='a'
    )

    SampleStreamBolt().run()