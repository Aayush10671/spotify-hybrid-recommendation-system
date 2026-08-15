import requests
import time

app_url = "http://localhost:8000"


def get_app_status(url):
    response = requests.get(url)

    status_code = response.status_code
    return status_code


def test_app_loading():

    time.sleep(60) 
    status_code = get_app_status(app_url)
    assert status_code == 200, "Unable to load the streamlit app"

    