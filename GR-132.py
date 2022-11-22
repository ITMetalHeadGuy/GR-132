import pika
import json

#def callback(ch, method, properties, body):
#    print('[x] Received data %r' % body.decode())
#    jsonOutput = json.loads(body.decode())
#    print(jsonOutput)
#    sortedList = jsonOutput["input"]
#    print('[x] Send data %r' % sorted(sortedList))
#    channel.stop_consuming()
    

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel=connection.channel()
#channel.basic_consume(exchange='output', queue='GR-132', on_message_callback=callback, body=sortedList)
jsonOutput = json.loads(channel.basic_get(queue='GR-132')[2].decode())
sortedList = jsonOutput["input"]
sortedList.sort()
channel.queue_declare(queue='output')
channel.basic_publish(exchange='', routing_key='output', body=bytearray(sortedList))
connection.close()