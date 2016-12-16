import pika
import time


connection = pika.BlockingConnection(
                                pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)

print("Waiting for messages...")

def callback(ch, method, properties, body):
    num = body.count(b'.')
    for i in range(num):
        print i, "%r"%body
        time.sleep(0.5)
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)     # tells to not accept more than one 
                                        #   task in queue at each time
channel.basic_consume(callback, queue='task_queue')

channel.start_consuming()
