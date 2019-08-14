from kafka import KafkaConsumer
consumer = KafkaConsumer('test')
for message in consumer:
    # print (message)
    # print (type(message))
    print (message.topic)
    print (message.timestamp)
    print (message.value)
    print (message.key)
    print()
