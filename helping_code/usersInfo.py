import requests
import json
import pprint
def get_users_emails():
    users_url = "https://aaas.atlas-ml.org/user/"
    response = requests.get(users_url)
    data = response.json()
    emails = [entry["_source"]["email"] for entry in data if "_source" in entry and "email" in entry["_source"]]
    # with open("helping_code/users.json", "w", encoding="utf-8") as file:
    #     json.dump(data, file, indent=4)
    return emails
# pprint.pprint(get_users_emails())

def get_users_ids():
    users_url = "https://aaas.atlas-ml.org/user/"
    response = requests.get(users_url)
    data = response.json()
    ids = [entry["_id"] for entry in data]
    # with open("helping_code/ids.json", "w", encoding="utf-8") as file:
    #     json.dump(data, file, indent=4)
    return ids
# pprint.pprint(get_users_ids())

def get_users_info():
    users_url = "https://aaas.atlas-ml.org/user/"
    response = requests.get(users_url)
    data = response.json()
    info = [entry for entry in data]
    with open("helping_code/users2.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)
    return info
# get_users_info()