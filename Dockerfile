FROM python:3.7-alpine
WORKDIR /code
ENV KAFKA_HOST=$KAFKA_HOST
ENV KAFKA_TOPIC=$KAFKA_TOPIC
RUN apk add --no-cache gcc musl-dev linux-headers
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD ["env"]
CMD [ "sh", "-c", "echo $KAFKA_HOST ($KAFKA_TOPIC)" ]
CMD ["python", "-u", "kafka_producer.py"]