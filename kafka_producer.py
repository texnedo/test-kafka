import sys
import time
from time import sleep
from json import dumps
from kafka import KafkaProducer


def main(connection: str):
    if connection is None or len(connection) == 0:
        connection = 'localhost:29092'
    print("Producer started with {}".format(connection))
    producer = KafkaProducer(bootstrap_servers=[connection],
                             key_serializer=lambda x: x.encode('utf-8'),
                             value_serializer=lambda x: dumps(x).encode('utf-8'))
    for i in range(0, 1000):
        text_index = str(i)
        meta = producer.send(topic="test-topic-some",
                             key="test-key-sync" + text_index,
                             value={"some_key" + text_index: "some_value" + text_index})
        print("Message sent:" + str(meta.args))
        time.sleep(0.1)
    producer.flush()


if __name__ == '__main__':
    main(sys.argv[1])
