#!/bin/bash

python3 /app/app.py &

until curl -s http://127.0.0.1:3000 > /dev/null; do
    echo "Waiting for Flask to start..."
    sleep 1
done

python3 /bot/bot.py
tail -f /dev/null
