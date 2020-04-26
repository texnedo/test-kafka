import sys

from kafka import KafkaConsumer
from json import loads


def main(connection: str):
    if connection is None or len(connection) == 0:
        connection = 'localhost:29092'
    print("Consumer started with {}".format(connection))
    consumer = KafkaConsumer(
        'test-topic-some',
        bootstrap_servers=['localhost:29092'],
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
    main(sys.argv[0])
