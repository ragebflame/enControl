# Replace libraries by fake ones
import sys
import fake_rpi
import thread

sys.modules['RPi'] = fake_rpi.RPi     # Fake RPi (GPIO)
sys.modules['RPi.GPIO'] = fake_rpi.RPi.GPIO # Fake RPi (GPIO)

# Call the script
#import enControl
#enControl.app.run(host = "0.0.0.0", port = 80, debug=True)


import os
import tempfile
import pytest

import enControl


@pytest.fixture
def client():
    client = enControl.app.test_client()
    yield client
    
def test_base_url(client):
    """Start with a blank database."""

    rv = client.get('/energenie-control/api/v1.0/gpio_pins')
    assert b'okay' in rv.data



        