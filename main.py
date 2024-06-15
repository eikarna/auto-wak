import requests
import time
from datetime import datetime, timedelta
import random
import string
import json
import sys

url = "https://api.wakatime.com/api/v1/users/current/heartbeats"

def random_string(length):
    return ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(length)])

def random_timestamp(max_days):
    now = datetime.now()
    random_days = random.randint(0, max_days)
    random_seconds = random.randint(0, 86400)  # Number of seconds in a day
    random_time = now + timedelta(days=random_days, seconds=random_seconds)
    return int((random_time - datetime(1970, 1, 1)).total_seconds())

def generate_payload(namefile, projectname, language):
    entity = "{}.go".format(random_string(8)) if namefile == "random" else namefile
    project = random_string(12) if projectname == "random" else projectname
    
    return {
        "type": "file",
        "entity": entity,
        "time": random_timestamp(180),
        "lineno": str(random.randint(1, 9999)),
        "cursorpos": str(random.randint(0, 99999)),
        "lines": str(random.randint(1, 9999)),
        "is_write": bool(random.getrandbits(1)),
        "plugin": random.choice(["vscode", "pycharm", "sublime", "micro", "nano"]),
        "project": project,
        "language": language,
        "project_root_count": random.randint(1, 10),
        "category": "coding"
    }

def main(apikey, namefile, projectname, language):
    querystring = {"api_key": apikey}
    headers = {
        "content-type": "application/json",
        "X-Machine-Name": "Windows"
    }
    
    while True:
        payload = generate_payload(namefile, projectname, language)
        response = requests.post(url, json=payload, headers=headers, params=querystring)
        print(json.dumps(response.json(), indent=2))
        time.sleep(1)

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python script.py <apikey> <namefile> <projectname> <language>")
        sys.exit(1)
    
    apikey = sys.argv[1]
    if len(apikey) < 1 or not "waka_" in apikey:
        print("Invalid API Key!")
        sys.exit(1)
    namefile = sys.argv[2]
    projectname = sys.argv[3]
    language = sys.argv[4]
    
    main(apikey, namefile, projectname, language)
