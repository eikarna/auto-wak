import requests
import time
from datetime import datetime, timedelta
import random
import string
import json

url = "https://api.wakatime.com/api/v1/users/current/heartbeats"
querystring = {"api_key": "waka_8a6ef3a2-4a62-4a76-a783-4249d8751d9a"}
headers = {
    "content-type": "application/json",
    "X-Machine-Name": "Windows"
}

def random_string(length):
    return ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(length)])

def random_timestamp(max_days):
    now = datetime.now()
    random_days = random.randint(0, max_days)
    random_seconds = random.randint(0, 86400)  # Number of seconds in a day
    random_time = now + timedelta(days=random_days, seconds=random_seconds)
    return int((random_time - datetime(1970, 1, 1)).total_seconds())

def generate_payload():
    return {
        "type": "file",
        "entity": "server.go", # "{}.go".format(random_string(8)),
        "time": time.time(),
        "lineno": str(random.randint(1, 9999)),
        "cursorpos": str(random.randint(0, 99999)),
        "lines": str(random.randint(1, 9999)),
        "is_write": bool(random.getrandbits(1)),
        "plugin": random.choice(["vscode", "pycharm", "sublime", "micro", "nano"]),
        "project": "gotps-enet",
        "language": "Go",
        "project_root_count": random.randint(1, 10),
        "category": "coding"
    }

while True:
    payload = generate_payload()
    response = requests.post(url, json=payload, headers=headers, params=querystring)
    print(json.dumps(response.json(), indent=2))
