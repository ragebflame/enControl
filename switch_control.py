import time
from flask import abort
import RPi.GPIO as GPIO


# Function that sends the command to the pins
def trigger_switch(data_mapping, parsed_switch_id):
    GPIO.setmode(GPIO.BOARD)  # set the pins numbering mode
    # time.sleep(0.25)
    # Select each of the GPIO pins needed
    needed_pins = [11, 15, 16, 13, 18, 22]
    data_pins = [11, 15, 16, 13]
    GPIO.setup(needed_pins, GPIO.OUT)  # Default all pin values to lo / 0
    GPIO.output(needed_pins, False)
    try:  # Loop to map all GPIO.outputs# Set K0 - K3(aka D0 - D3)
        for i in range(0, len(data_pins)):
            GPIO.output(data_pins[i], data_mapping[i])

        time.sleep(0.25)  # let it settle, encoder requires this
        GPIO.output(22, True)  # Enable the modulator
        time.sleep(0.25)  # keep enabled for a period
        GPIO.output(22, False)  # Disable the modulator
    except Exception:
        print("Error trying to send the command. Exiting.")
        abort(500)

    # Clean up the GPIOs for next time
    GPIO.cleanup()
    print("Command sent sucessfully for " + parsed_switch_id)
