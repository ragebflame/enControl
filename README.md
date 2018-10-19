
<h1 align="center">enControl.py</h1>
<h4 align="center">Python flask API for controlling energenie pi-mote on raspberry pi</h4>

<p align="center">
  <a href="https://travis-ci.org/ragebflame/enControl">
    <img src="https://travis-ci.org/ragebflame/enControl.svg?branch=master">
  </a>
  <a href="https://www.python.org/">
    <img src="https://img.shields.io/badge/Made%20with-Python-1f425f.svg">
  </a>
  <a href="https://github.com/ragebflame/enControl/issues">
    <img src="https://img.shields.io/github/issues/Naereen/StrapDown.js.svg">
  </a>
  <a href="https://github.com/ragebflame/enControl/blob/master/LICENSE">
    <img src="https://img.shields.io/github/license/Naereen/StrapDown.js.svg">
  </a>  
</p>

## What does this do?
This is a Python script which interacts with an energenie pi-mote using a flask api. This will allow you to turn sockets on & off with rest requests.

###### Why?
I had the hardware, and I needed an easy way to call the sockets from a [Home Assistant](https://www.home-assistant.io/) instance on a separate machine.

## Okay cool! let's get started

These instructions will get you a copy of the project up and running on your Raspberry Pi.

Here is what you will need:
#### Hardware
 - Raspberry pi (I'm using an RPI1 model B+)
 - The pi-mote board
https://energenie4u.co.uk/catalogue/product/ENER314
 - The energenie sockets
https://energenie4u.co.uk/catalogue/product/ENER002-4

For more info on interfacing with the pi-mote check the [energenie website](https://www.home-assistant.io/).

#### Software
 - Python (2.7) & required packages
  - flask
  - RPi.GPIO

## Installation

### Automated install

```
wget https://raw.githubusercontent.com/ragebflame/enControl/master/install.sh && chmod +x install.sh && ./install.sh
```
### Manual install
For **Debian** based distros:
```
$ sudo apt update && sudo apt upgrade -y
$ sudo apt install git python pip
$ git clone https://github.com/ragebflame/enControl
$ cd enControl && sudo pip install -r requirements.txt
```

## Run
```
$ sudo python enControl.py
```
server running:
```
$ sudo python enControl.py
 * Serving Flask app "enControl" (lazy loading)
 * Environment: production
   WARNING: Do not use the development server in a production environment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://0.0.0.0:80/ (Press CTRL+C to quit)
```
#### REST requests:
Available `POST` requests

| id  | commands |
| --- |:--------:|
|  `1`  | `on` / `off` |
|  `2`  | `on` / `off` |
|  `3`  | `on` / `off` |
|  `4`  | `on` / `off` |
| `all` | `on` / `off` |

Check API
```
$ curl -i localhost/energenie-control/api/v1.0/gpio_pins
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 25
Server: Werkzeug/0.14.1 Python/2.7.6
Date: Fri, 19 Oct 2018 12:21:06 GMT
```
Turn socket 3 on
```
curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"id":"3","command":"on"}' \
  localhost/energenie-control/api/v1.0/gpio_pins
```



#### Run on startup
To run the flask server on startup, add the following to the **/etc/rc.local** file before the "exit 0"
```
# Start the flask server
sudo python /home/pi/enControl/enControl.py &

exit 0
```

## Tasks

- [x] Implement Travis-CI
- [x] Re-factor code using Flake8 linter
- [x] Add an auto-install script
- [ ] Add Home assistant config
- [ ] Expand unit test coverage
- [ ] Add install steps for Arch based distros
- [ ] Add additional functionality
- [ ] Improve this readme :eyes:

## Contributing
Why not open a Pull Request, or  
[![Buy me a coffee](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/6KqDHIdO4)
