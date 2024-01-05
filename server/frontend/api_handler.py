import os
import requests
import logging

BASE_API_URL = os.environ.get("BASE_API_URL") or "http://localhost"
API_PORT = os.environ.get("API_PORT") or "8000"


def send_file_to_api(uploaded_file):
    try:
        url = f"{BASE_API_URL}:{API_PORT}/uploadCustomDoc"
        files = {"file": (uploaded_file.name, uploaded_file.read(), uploaded_file.type)}

        response = requests.post(url, files=files)
        if response.status_code != 200:
            return False
        else:
            return True

    except Exception as e:
        logging.error(e)
        return False
