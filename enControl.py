#!flask/bin/python
from flask import Flask, jsonify, abort, make_response, request
from redis import Redis
from rq import Queue, Worker, Connection
from switch_control import trigger_switch
#import RPi.GPIO as GPIO
import time

app = Flask(__name__)

# Mapping a dictionary of gpio values as json
gpio_values = {
    'switch': [{
        'id': u'1',
        'command': [{
            'on': [True, True, True, True],
            'off': [True, True, True, False]
            }],
        }, {
        'id': u'2',
        'command': [{
            'on': [False, True, True, True],
            'off': [False, True, True, False]
            }],
        }, {
        'id': u'3',
        'command': [{
            'on': [True, False, True, True],
            'off': [True, False, True, False]
            }],
        }, {
        'id': u'4',
        'command': [{
            'on': [False, False, True, True],
            'off': [False, False, True, False]
            }],
        }, {
        'id': u'all',
        'command': [{
            'on': [True, True, False, True],
            'off': [True, True, False, False]
            }]
        }]
}

# Define the task Queue
request_queue = Queue(connection=Redis())
# Define a worker
worker = Worker(request_queue, connection=Redis())
worker.work()

# Return the gpio_pins dictionary
@app.route('/energenie-control/api/v1.0/gpio_pins', methods=['GET'])
def get_gpio_pins():
    return jsonify({
        'Everything': 'is okay'
        })


# Return info on particular switch
@app.route('/energenie-control/api/v1.0/gpio_pins/<switch_id>', methods=['GET'])
def get_switch(switch_id):
    switch = [switch for switch in gpio_values["switch"]
              if switch["id"] == switch_id]

    if len(switch) == 0:
        abort(404)
    return jsonify({'switch': switch[0]})


# Send command to specified switch
@app.route('/energenie-control/api/v1.0/gpio_pins', methods=['POST'])
def post_command():
    # verify and sanitize the received json
    if (not request.json
            or 'id' not in request.json or 'command' not in request.json):
        abort(400)

    parsed_switch_id = request.json['id']
    parsed_switch_command = request.json['command']

    for switch in gpio_values['switch']:
        if switch['id'] == parsed_switch_id:
            for commands in switch['command']:
                data_mapping = commands[parsed_switch_command]

    if len(data_mapping) == 0:
        abort(500)

    print(data_mapping)

    # Send command to the switch
    #trigger_switch(data_mapping, parsed_switch_id)

    # Enqueue the function call
    #result = request_queue.Enqueue(trigger_switch, data_mapping, parsed_switch_id)
    request_queue.enqueue(trigger_switch, data_mapping, parsed_switch_id)

    # Return an OK
    return jsonify(request.json), 202


# handle 404 errors gracefully
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({
        'error': 'Not found'
        }), 404)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
