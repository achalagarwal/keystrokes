#!/bin/sh


# launch the dbus server for notifications
nohup sudo /home/achal/.python_environments/keyboard/bin/python3 src/notifs.py &

# launch the main python script
nohup sudo /home/achal/.python_environments/keyboard/bin/python3 src/__main__.py &
