import requests

BASE_URL = "http://127.0.0.1:8000"
city = input()
i = 0
while True:
    i += 1
    response = requests.get(f"{BASE_URL}/vacancies/{i}")
    if response.json()['area_name'] == city:
        print(response.json())
    if i == 100:
        break