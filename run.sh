#!/bin/bash

if [ ! -d "venv" ]; then
    python3 -m venv venv
    source venv/bin/activate 
    pip install -r requirements.txt
    pip install gunicorn
fi

source venv/bin/activate

gunicorn -w 2 -b 127.0.0.1:5001 app:app

echo "If Something goes wrong with the dependency, try running 'pip install -r requirements.txt' manually."