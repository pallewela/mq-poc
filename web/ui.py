import json
import uuid
import pika
from flask import Flask, request, render_template, redirect, url_for, jsonify

app = Flask(__name__)

@app.route("/ui")
def ui():
    return render_template('inputform.html')

@app.route("/api/scrape", methods=['POST'])
def do_scrape():
    task = {}
    task['id'] = str(uuid.uuid1())
    task['callback'] = "http://test_ui:5000/scraper-callback/%s" % task['id']
    task['message'] = request.form['text'] or "Empty Task!"
    

    #TODO: take rabbitmq params from env
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='test-rabbit')) 
    channel = connection.channel()
    channel.queue_declare(queue='task_queue', durable=True)

    message = json.dumps(task)
    channel.basic_publish(
            exchange='',
            routing_key='task_queue',
            body=message,
            properties=pika.BasicProperties(
                delivery_mode=2,#persistent
            )
    )

    print(" Message Queued: %s" % message)
    return '<p>Scrape Requested: %s</p><p><a href="http://localhost:5000/ui">Request again</a></p>' % message

@app.route("/scraper-callback/<uuid>", methods=['POST'])
def scrape_callback(uuid):
    data = request.json
    print(" Recieved response for uuid[%s]: %s" % (uuid, data))
    return jsonify(success=True)

@app.route("/")
def root():
    return redirect(url_for('ui'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int("5000"), debug=False, use_reloader=False)
