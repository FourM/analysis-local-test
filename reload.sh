#!/bin/bash

# No exec local

git pull
PORT=`ps aux | grep -m1 gunicorn | awk {'print $2'}`
kill -HUP $PORT
