
import pika
import sys

connection = pika.BlockingConnection(
                pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# fanout = broadcasts the message to all the queues the exchange knows.
# Theses queues will be declared in the suscribers.
channel.exchange_declare(exchange='logs', type='fanout')

message = ' '.join(sys.argv[1:]) or "info: Hello World!"

# Precise the name of the exchange to which send the messages (that then
# will be sent to its queues)
channel.basic_publish(exchange='logs',
                      routing_key='',
                      body=message)

print(" [x] Sent %r" % message)

connection.close()
