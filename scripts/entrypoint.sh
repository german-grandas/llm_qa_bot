#!/bin/bash

if [ "$1" == "socket" ]; then
    exec poetry run python chat_socket_server.py
elif [ "$1" == "api" ]; then
    exec poetry run uvicorn api:app --host 0.0.0.0 --port $API_PORT

elif [ "$1" == "front" ]; then
    exec poetry run streamlit run ./frontend/app.py
else
    echo "Invalid command. Please use 'api' or 'socket'."
    exit 1
fi