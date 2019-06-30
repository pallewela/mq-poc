import pika
import time
import json
import requests

def callback(channel, method, properties, body): 
    #ack as soon as a task is picked. errors needs to be looked into manually. 
    channel.basic_ack(delivery_tag=method.delivery_tag)
    print(" Received task: %s" % body)
    
    task = json.loads(body)
    try:
        time_to_sleep = int(task['message'])
    except:
        time_to_sleep = 1;

    time.sleep(time_to_sleep)
    print(" sending scraper result for: %s" % task['id'])
    requests.post(task['callback'], json={'result':'scrape result'})


#TODO get rabbitmq config from env
connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='test-rabbit'))
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)
print(' Listening task_queue for tasks')

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='task_queue', on_message_callback=callback)
channel.start_consuming()
