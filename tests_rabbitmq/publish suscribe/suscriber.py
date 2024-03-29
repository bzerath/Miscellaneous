import pika

connection = pika.BlockingConnection(
                    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# fanout = broadcasts the message to all the queues the exchange knows.
channel.exchange_declare(exchange='logs', type='fanout')

# If we disconnect the consumer, the queue should be deleted
result = channel.queue_declare(exclusive=True)

queue_name = result.method.queue
# Bind the queue of <result> to the exchange 'logs'
channel.queue_bind(exchange='logs', queue=queue_name)

print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print(" [x] %r" % body)

channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)

channel.start_consuming()


