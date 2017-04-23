#!/usr/bin/env python
"""
USAGE: python suscriber.py [info] and/or [warning] and/or [error]
example:
>>> python info warning
--> listens only "info" and "warning"

"""
import pika
import sys

connection = pika.BlockingConnection(
                pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# direct = takes into account binding keys
channel.exchange_declare(exchange='direct_logs', type='direct')

# If we disconnect the consumer, the queue should be deleted
result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

# gets severities that wiil be taken into account into this suscriber
severities = sys.argv[1:]
if not severities:
    sys.stderr.write("Usage: %s [info] [warning] [error]\n" % sys.argv[0])
    sys.exit(1)

# For each severity received, binds the queue to its related routing key
for severity in severities:
    channel.queue_bind(exchange='direct_logs',
                       queue=queue_name,
                       routing_key=severity)

print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print(" [x] %r:%r" % (method.routing_key, body))

channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)

channel.start_consuming()
