#!/bin/bash

if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

source venv/bin/activate

pip install -r requirements.txt
pip install gunicorn

gunicorn -w 2 -b 127.0.0.1:5001 app:app