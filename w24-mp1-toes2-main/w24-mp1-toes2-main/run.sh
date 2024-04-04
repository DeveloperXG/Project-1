#!/bin/bash

if [ ! -d "venv" ]; then
	echo "Creating a virtual environment for you..."
	python3 -m venv venv
	. venv/bin/activate
	pip3 install flask
fi

if [ $# -eq 0 ]; then
    echo "App requires database path"
    echo "Usage: ./run.sh [path to database]"
else
	export APP_DB_PATH=$1
	echo "Running app..."
	. venv/bin/activate
	flask run
fi
