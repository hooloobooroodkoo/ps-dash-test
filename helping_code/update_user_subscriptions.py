from elastic import ConnectES
from usersInfo import get_users_ids, get_users_info
from elasticsearch.helpers import scan

global description, reverse_mapping
description = {
        'Infrastructure': ['bad owd measurements', 'large clock correction', "indexing",
                           'destination cannot be reached from multiple', 'destination cannot be reached from any',
                           'source cannot reach any', 'firewall issue', 'complete packet loss',
                           'unresolvable host', 'hosts not found'],
        'Network': ['bandwidth decreased from/to multiple sites', 'path changed between sites',
                    'ASN path anomalies', 'path changed'],
        'Other': ['bandwidth increased from/to multiple sites', 'bandwidth increased', 'bandwidth decreased',
                  'high packet loss', 'high packet loss on multiple links']
    }
reverse_mapping = {value: key for key, values in description.items() for value in values}

def update_user_subscriptions(es, user_id):
    #extract user's data from Elasticsearch
    query = {
        "query": {
            "term": {
                "_id": user_id
            }
        }
    }

    data = scan(es, index="aaas_users", query=query)
    print(data)
    user_data = list(data)
    print(user_data)
    
    if not user_data:
        print("User not found.")
        return None
    
    all_events = reverse_mapping.keys()
    print("\n*************BEFORE*************")
    print(user_data[0]["_source"]["subscriptions"])
    for subscription in user_data[0]["_source"]["subscriptions"]:
        try:
            event = subscription["event"].lower()
            if event == "firewall issue":
                subscription["event"] = event
            if event in all_events:
                subscription["category"] = "Networking"
                subscription["subcategory"] = reverse_mapping[event]
        except Exception as err:
            print("No subscriptions!?", err)
    print("\n*************CHANGED*************")
    print(user_data[0]["_source"]["subscriptions"])
    updated_body = {
        "doc": {
            "preferences": user_data[0]["_source"].get("preferences", {}),
            "subscriptions": user_data[0]["_source"]["subscriptions"]
        }
    }
    # update user doc by _id
    es.update(index="aaas_users", id=user_id, body=updated_body)
    
    # verify the update
    updated_data = es.get(index="aaas_users", id=user_id)
    print(updated_data["_source"])  # Print the updated document


def changeUserSubs(es, user_id):
    
    # find the user
    query = {
        "query": {
            "term": {
                "_id": user_id
            }
        }
    }
    
    data = scan(es, index="aaas_users", query=query)
    user_data = list(data)
    
    if not user_data:
        print("User not found.")
        return None
    
    # updated subscription body
    update_body = {
        "doc": {
            "preferences": {
                "vacation": False,
                "mail_interval": 1,
                "prefered_mail": ""
            },
            "subscriptions": [
                {
                "category": "Networking",
                "subcategory": "Infrastructure",
                "event": "bad owd measurements",
                "tags": "*"
            },
            {
                "category": "Networking",
                "subcategory": "Infrastructure",
                "event": "large clock correction",
                "tags": "*"
            },
            {
                "category": "Networking",
                "subcategory": "Infrastructure",
                "event": "firewall issue",
                "tags": "*"
            },
            {
                "category": "Networking",
                "subcategory": "Infrastructure",
                "event": "complete packet loss",
                "tags": "*"
            },
            {
                "category": "Networking",
                "subcategory": "Infrastructure",
                "event": "unresolvable host",
                "tags": "*"
            },
            {
                "category": "Networking",
                "subcategory": "Infrastructure",
                "event": "indexing",
                "tags": "*"
            },
            {
                "category": "Networking",
                "subcategory": "Infrastructure",
                "event": "destination cannot be reached from multiple",
                "tags": "*"
            },
            {
                "category": "Networking",
                "subcategory": "Infrastructure",
                "event": "destination cannot be reached from any",
                "tags": "*"
            },
            {
                "category": "Networking",
                "subcategory": "Other",
                "event": "bandwidth increased from/to multiple sites",
                "tags": "*"
            },
            {
                "category": "Networking",
                "subcategory": "Network",
                "event": "bandwidth decreased from/to multiple sites",
                "tags": "*"
            },
            {
                "category": "Networking",
                "subcategory": "Other",
                "event": "high packet loss",
                "tags": "*"
            },
            {
                "category": "Networking",
                "subcategory": "Infrastructure",
                "event": "source cannot reach any",
                "tags": "*"
            },
            {
                "category": "Networking",
                "subcategory": "Other",
                "event": "bandwidth increased",
                "tags": "*"
            },
            {
                "category": "Networking",
                "subcategory": "Other",
                "event": "bandwidth decreased",
                "tags": "*"
            },
            {
                "category": "Networking",
                "subcategory": "Network",
                "event": "path changed",
                "tags": "*"
            }
            ]
        }
    }
    
    # update user doc by _id
    es.update(index="aaas_users", id=user_id, body=update_body)
    
    # verify the update
    updated_data = es.get(index="aaas_users", id=user_id)
    print(updated_data["_source"])  # Print the updated document
    
    return updated_data


connection = ConnectES()
# all_users_ids = get_users_ids()
# for user in all_users_ids:
#     update_user_subscriptions(connection, user)
# get_users_info()
changeUserSubs(connection, "3ad018e2-ef67-44d1-b48f-f46f808bfe69")