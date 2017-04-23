import pika
import sys
import time
import random


for num in range(1, 30):
    length = random.randint(1, 30)
    connection = pika.BlockingConnection(
                                    pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='task_queue', durable=True)

    message = "Message {id} {dots}".format(id=num,
                                           dots="."*length)
    channel.basic_publish(exchange='',
                          routing_key='task_queue',
                          body=message,
                          properties=pika.BasicProperties(
                                    delivery_mode=2,  # make message persistent
                          ))
    print(" [x] Sent %r" % message)
    connection.close()
    time.sleep(1)
