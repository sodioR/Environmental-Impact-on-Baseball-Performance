import json
import requests

if __name__ == "__main__":

    print("Calling API server...")
    url = 'http://fastapi:8000/weather/Oriole%20Park%20at%20Camden%20Yards/2023-07-05/'
    headers = {
        'Content-Type': 'application/json'
    }

    print("Making GET request to API...")
    response = requests.get(url, headers=headers)
    print(response.status_code)
    print(json.loads(response.content))

    print("Making second GET request to API...")
    url = 'http://fastapi:8000/pitchers/'
    headers = {
        'Content-Type': 'application/json'
    }

    response2 = requests.get(url, headers=headers)
    print(response2.status_code)
    print(json.loads(response2.content))