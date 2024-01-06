import requests

BASE_URL = "http://127.0.0.1:8000"

name, salary, area_name = input(), input(), input()

new_vacancy = {
    "name": name,
    "salary": salary,
    "area_name": area_name
}

response = requests.post(f"{BASE_URL}/vacancies", json=new_vacancy)
print(response.json())