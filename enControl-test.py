# Replace libraries by fake ones
import sys
import fake_rpi

sys.modules['RPi'] = fake_rpi.RPi     # Fake RPi (GPIO)
sys.modules['RPi.GPIO'] = fake_rpi.RPi.GPIO # Fake RPi (GPIO)
# Call the script
import enControl
enControl.app.run(host = "0.0.0.0", port = 80)