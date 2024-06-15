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
    entity = "{}.{}".format(random_string(8), eksfile) if namefile == "random" else "{}.{}".format(namefile, eksfile)
    project = random_string(12) if projectname == "random" else projectname
    
    return {
        "type": "file",
        "entity": entity,
        "time": time.time(),
        "lineno": str(random.randint(1, 9999)),
        "cursorpos": str(random.randint(0, 99999)),
        "lines": str(random.randint(1, 9999)),
        "line_additions": str(random.randint(1, 9999)),
        "line_deletions": str(random.randint(1, 9999)),
        "is_write": bool(random.getrandbits(1)),
        "plugin": random.choice(["vscode", "pycharm", "sublime", "nano", "micro", "jetbrains"]),
        "project": project,
        "language": language,
        "project_root_count": random.randint(1, 10),
        "category": random.choice(["coding", "building", "indexing", "debugging", "browsing", "running tests", "writing tests", "manual testing", "writing docs", "communicating", "code reviewing", "researching", "learning", "designing"]),
        "hostname": "Windows",
        "branch": "main"
    }

def main(apikey, namefile, eksfile, projectname, language):
    querystring = {"api_key": apikey}
    headers = {
        "Content-Type": "application/json",
        "X-Machine-Name": platform.node()
    }
    
    try:
        while True:
            try:
                payload = generate_payload(namefile, eksfile, projectname, language)
                response = requests.post(url, json=payload, headers=headers, params=querystring, timeout=1500)
                print(json.dumps(response.json(), indent=2))
                time.sleep(1)
            except Exception as e:
                print(f"An error occurred: {e}")
                pass
    except KeyboardInterrupt:
        print("\nProgram interrupted by user. Exiting...")

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
