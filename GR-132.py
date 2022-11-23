import pika
import json

def callback(ch, method, properties, body):
    print('[x] Received data %r' % body.decode())
    jsonOutput = json.loads(body.decode())
    sortedList = jsonOutput["input"]
    ch.basic_publish(exchange='output', routing_key='', properties=properties, body=json.dumps({'input':sorted(sortedList)}))
    print('[x] Send data %r' % sorted(sortedList))
    

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel=connection.channel()
channel.exchange_declare(exchange='input', exchange_type='fanout')
result=channel.queue_declare(queue='', exclusive=True)
queue_name=result.method.queue
channel.queue_bind(exchange='input', queue=queue_name)
trying=channel.basic_consume(queue=queue_name, on_message_callback=callback)
channel.start_consuming()
#while channel.basic_get(queue='input') != "":
#    jsonOutput = json.loads(channel.basic_get(queue='input')[2].decode())
#    sortedList = jsonOutput["input"]
#    sortedList.sort()
#    channel.queue_declare(queue='input')
#    print(sorted(sortedList))
#    channel.basic_publish(exchange='', routing_key='output', body=bytearray(sortedList))
#    connection.close()
