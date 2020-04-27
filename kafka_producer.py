import os
import time
from json import dumps
from kafka import KafkaProducer
from kafka.errors import KafkaError


def main(connection: str, topic: str):
    if connection is None or len(connection) == 0:
        connection = 'localhost:29092'
    if topic is None or len(topic) == 0:
        topic = 'test-topic-some'
    print("Producer started with {} for topic {}".format(connection, topic))
    for loop_index in range(0, 1000):
        try:
            print("Try connect to kafka {}".format(connection))
            producer = KafkaProducer(bootstrap_servers=[connection],
                                     key_serializer=lambda x: x.encode('utf-8'),
                                     value_serializer=lambda x: dumps(x).encode('utf-8'))
            for i in range(0, 1000):
                text_index = str(i)
                meta = producer.send(topic=topic,
                                     key="test-key" + text_index,
                                     value={"some_key" + text_index: "some_value" + text_index})
                print("Message sent:" + str(meta.args))
                time.sleep(0.1)
            producer.flush()
        except Exception as ex:
            print("Kafka connection error on loop index {} due to {}".format(loop_index, ex))
            time.sleep(1)


if __name__ == '__main__':
    main(os.environ['KAFKA_HOST'] if 'KAFKA_HOST' in os.environ else "",
         os.environ['KAFKA_TOPIC'] if 'KAFKA_TOPIC' in os.environ else "")
