import sys
import fake_rpi
import pytest
# Replace libraries by fake ones
sys.modules['RPi'] = fake_rpi.RPi  # Fake RPi (GPIO)
sys.modules['RPi.GPIO'] = fake_rpi.RPi.GPIO  # Fake RPi (GPIO)

# Now import the script
import enControl


# Define pytest cases
@pytest.fixture
def client():
    client = enControl.app.test_client()
    yield client


def test_base_url(client):
    """Start with a blank database."""

    rv = client.get('/energenie-control/api/v1.0/gpio_pins')
    assert b'okay' in rv.data
