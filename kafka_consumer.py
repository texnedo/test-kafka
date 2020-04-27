import os
import sys

from kafka import KafkaConsumer
from json import loads


def main(connection: str, topic: str):
    if connection is None or len(connection) == 0:
        connection = 'localhost:29092'
    if topic is None or len(topic) == 0:
        topic = 'test-topic-some'
    print("Consumer started with {} for topic {}".format(connection, topic))
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=[connection],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='my-group-new',
        key_deserializer=lambda x: safe_deserialize_key(x),
        value_deserializer=lambda x: safe_deserialize_value(x))
    for message in consumer:
        if message.key is not None and len(message.key) != 0:
            print("Received message {}: {}".format(message.key, message.value))


def safe_deserialize_value(data: bytearray):
    try:
        result = loads(data.decode('utf-8'))
        return result
    except Exception as ex:
        print("Failed to decode message: {}".format(ex))
        return ""


def safe_deserialize_key(data: bytearray):
    try:
        result = data.decode('utf-8')
        return result
    except Exception as ex:
        print("Failed to decode message: {}".format(ex))
        return ""


if __name__ == '__main__':
    main(os.environ['KAFKA_HOST'] if 'KAFKA_HOST' in os.environ else "",
         os.environ['KAFKA_TOPIC'] if 'KAFKA_TOPIC' in os.environ else "")
