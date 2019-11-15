#!/bin/bash

echo "
             ____            _             _               
  ___ _ __  / ___|___  _ __ | |_ _ __ ___ | |  _ __  _   _ 
 / _ \ '_ \| |   / _ \| '_ \| __| '__/ _ \| | | '_ \| | | |
|  __/ | | | |__| (_) | | | | |_| | | (_) | |_| |_) | |_| |
 \___|_| |_|\____\___/|_| |_|\__|_|  \___/|_(_) .__/ \__, |
            Install script                    |_|    |___/ 
"

debian_install() {
    sudo apt update && sudo apt upgrade -y
    sudo apt install git python pip redis-server
}

python_setup() {
    git clone https://github.com/ragebflame/enControl
    cd enControl && sudo pip install -r requirements.txt

    echo  "Installation complete!"
}

if [ "$(grep -Ei 'debian|ubuntu|mint' /etc/*release)" ]; then
    debian_install
    python_setup
else
    echo "Only Debian based distros are supported at the moment."
fi