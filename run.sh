#!/bin/bash
echo "Do not run this as a production server!"

export FLASK_ENV='dev'
export FLASK_DEBUG=1
export FLASK_SECRET_KEY="NotSoSecretKey"

source venv/bin/activate && python3 app.py