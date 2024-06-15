import requests
import time
from datetime import datetime, timedelta
import random
import string
import json
import sys
import platform

url = "https://api.wakatime.com/api/v1/users/current/heartbeats"

def random_string(length):
    return ''.join([random.choice(string.ascii_letters + string.digits) for _ in range(length)])

def generate_payload(namefile, eksfile, projectname, language):
    entity = "{}.{}".format(random_string(8)) if namefile == "random" else namefile.format(eksfile)
    project = random_string(12) if projectname == "random" else projectname
    
    return {
        "type": "file",
        "entity": entity,
        "time": time.time(),
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

def main(apikey, namefile, eksfile, projectname, language):
    querystring = {"api_key": apikey}
    headers = {
        "Content-Type": "application/json",
        "X-Machine-Name": platform.node()
    }
    
    while True:
        payload = generate_payload(namefile, eksfile, projectname, language)
        response = requests.post(url, json=payload, headers=headers, params=querystring)
        print(json.dumps(response.json(), indent=2))
        time.sleep(1)

if __name__ == "__main__":
    if len(sys.argv) != 6:
        print("Usage: python script.py <apikey> <namefile> <extensionfile> <projectname> <language>")
        sys.exit(1)
    
    apikey = sys.argv[1]
    if len(apikey) < 1 or not "waka_" in apikey:
        print("Invalid API Key!")
        sys.exit(1)
    namefile = sys.argv[2]
    eksfile = sys.argv[3]
    projectname = sys.argv[4]
    language = sys.argv[5]
    
    main(apikey, namefile, eksfile, projectname, language)
