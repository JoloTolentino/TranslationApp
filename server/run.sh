#!/bin/usr/env bash

export FLASK_APP=wsgi
export FLASK_ENV=development
export FLASK_DEBUG=1 
# echo "Running Flask Server in the background"
flask run --no-reload 


