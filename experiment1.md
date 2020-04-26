#Check running instances
```bash
docker ps
CONTAINER ID        IMAGE                      COMMAND                  CREATED             STATUS              PORTS                                              NAMES
e47c504e372a        bitnami/kafka:latest       "/opt/bitnami/script…"   3 hours ago         Up 3 hours          0.0.0.0:9092->9092/tcp, 0.0.0.0:29092->29092/tcp   kafka-server
8a649358f3f6        bitnami/zookeeper:latest   "/opt/bitnami/script…"   3 hours ago         Up 3 hours          2181/tcp, 2888/tcp, 3888/tcp, 8080/tcp             zookeeper-server
```
#Run another instance
```bash
docker run -d --name kafka-server-2 \
    --network test-kafka-net \
    -e KAFKA_CFG_AUTO_CREATE_TOPICS_ENABLE=true \
    -e ALLOW_PLAINTEXT_LISTENER=yes \
    -e KAFKA_CFG_ZOOKEEPER_CONNECT=zookeeper-server:2181 \
    -e KAFKA_CFG_LISTENER_SECURITY_PROTOCOL_MAP=PLAINTEXT:PLAINTEXT,PLAINTEXT_HOST:PLAINTEXT \
    -e KAFKA_CFG_LISTENERS=PLAINTEXT://:9093,PLAINTEXT_HOST://:29093 \
    -e KAFKA_CFG_ADVERTISED_LISTENERS=PLAINTEXT://kafka-server-2:9093,PLAINTEXT_HOST://localhost:29093 \
    -p 9093:9093 \
    -p 29093:29093 \
    bitnami/kafka:latest
```
#Send some new keys 'test-key-sync' to 'kafka-server' with kafka_producer.py
```bash
docker ps
CONTAINER ID        IMAGE                      COMMAND                  CREATED             STATUS              PORTS                                                        NAMES
520007d3afcb        bitnami/kafka:latest       "/opt/bitnami/script…"   2 minutes ago       Up 2 minutes        0.0.0.0:9093->9093/tcp, 9092/tcp, 0.0.0.0:29093->29093/tcp   kafka-server-2
e47c504e372a        bitnami/kafka:latest       "/opt/bitnami/script…"   3 hours ago         Up 3 hours          0.0.0.0:9092->9092/tcp, 0.0.0.0:29092->29092/tcp             kafka-server
8a649358f3f6        bitnami/zookeeper:latest   "/opt/bitnami/script…"   3 hours ago         Up 3 hours          2181/tcp, 2888/tcp, 3888/tcp, 8080/tcp                       zookeeper-server
```
#Stop 'kafka-server'
```bash
docker stop 520007d3afcb
docker start 520007d3afcb
docker stop e47c504e372a
```
#Try to read from 'kafka-server-2' with kafka_consumer.py