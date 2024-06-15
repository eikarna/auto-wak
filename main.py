import time
import random
import string
import json
import sys
import platform
import requests

URL = "https://api.wakatime.com/api/v1/users/current/heartbeats"


def random_string(length):
    return "".join(
        [random.choice(string.ascii_letters + string.digits) for _ in range(length)]
    )


def generate_payload(namefile, eksfile, projectname, language):
    entity = (
        f"{random_string(8)}.{eksfile}"
        if namefile == "random"
        else f"{namefile}.{eksfile}"
    )
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
        "plugin": random.choice(
            ["vscode", "pycharm", "sublime", "nano", "micro", "jetbrains"]
        ),
        "project": project,
        "language": language,
        "project_root_count": random.randint(1, 99),
        "category": random.choice(
            [
                "coding",
                "building",
                "indexing",
                "debugging",
                "browsing",
                "running tests",
                "writing tests",
                "manual testing",
                "writing docs",
                "communicating",
                "code reviewing",
                "researching",
                "learning",
                "designing",
            ]
        ),
        "hostname": "Windows",
        "branch": "main",
    }


def main(apikey, namefile, eksfile, projectname, language):
    querystring = {"api_key": apikey}
    headers = {"Content-Type": "application/json", "X-Machine-Name": platform.node()}

    try:
        while True:
            try:
                payload = generate_payload(namefile, eksfile, projectname, language)
                response = requests.post(
                    URL, json=payload, headers=headers, params=querystring, timeout=1500
                )
                print(json.dumps(response.json(), indent=2))
                time.sleep(1)
            except requests.exceptions.RequestException as err:
                print(f"An error occurred when sending request: {err}")

    except KeyboardInterrupt:
        print("\nProgram interrupted by user. Exiting...")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 6:
        print(
            "Usage: python script.py <apikey> <namefile> <extensionfile> <projectname> <language>"
        )
        sys.exit(1)

    a = sys.argv[1]
    if len(a) < 1 or not "waka_" in a:
        print("Invalid API Key!")
        sys.exit(1)
    b = sys.argv[2]
    c = sys.argv[3]
    d = sys.argv[4]
    e = sys.argv[5]

    main(a, b, c, d, e)
