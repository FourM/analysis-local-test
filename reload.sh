#!/bin/bash

# GCE内サーバー再起動
PORT=`ps aux | grep -m1 gunicorn | awk {'print $2'}`
kill -HUP $PORT
