#!flask/bin/python

from flask import Flask, jsonify, abort, make_response, request
import RPi.GPIO as GPIO
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

# Return the gpio_pins dictionary
@app.route('/energenie-control/api/v1.0/gpio_pins', methods = ['GET'])
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
    if not request.json or not 'id' in request.json or not 'command' in request.json:
        abort(400)
    
    parsed_switch_id = request.json['id']
    parsed_switch_command = request.json['command']

    for switch in gpio_values['switch']:
        if switch['id'] == parsed_switch_id:
            for commands in switch['command']:
                data_mapping = commands[parsed_switch_command]
                
    if len(data_mapping) == 0:
        abort(500)
        
    print data_mapping
    
    # Send command to the switch
    
    trigger_switch(data_mapping)
    # replace the gpio_mapping with the json mapping from received json
    
    # Return an OK 
    return jsonify(request.json), 202

# handle 404 errors gracefully
@app.errorhandler(404)
def not_found(error):
  return make_response(jsonify({
    'error': 'Not found'
  }), 404)

# Function that sends the command to the pins
def trigger_switch(data_mapping):
    GPIO.setmode(GPIO.BOARD) # set the pins numbering mode
    
    # Select each of the GPIO pins needed
    needed_pins = [11, 15, 16, 13, 18, 22]
    data_pins = [11, 15, 16, 13]
    GPIO.setup(needed_pins, GPIO.OUT)# Default all pin values to lo / 0
    GPIO.output(needed_pins, False)
    try: #Loop to map all GPIO.outputs# Set K0 - K3(aka D0 - D3)
        for i in range(0, len(data_pins)):
          GPIO.output(data_pins[i], data_mapping[i])
        
        time.sleep(0.25) # let it settle, encoder requires this
        GPIO.output(22, True) # Enable the modulator
        time.sleep(0.25) # keep enabled for a period
        GPIO.output(22, False) # Disable the modulator
    except:
      print "Error trying to send the command. Exiting."
      abort(500)
    
    # Clean up the GPIOs for next time
    GPIO.cleanup()
    print "Command sent sucessfully!"  

if __name__ == '__main__':
  app.run(host = "0.0.0.0", port = 80)
