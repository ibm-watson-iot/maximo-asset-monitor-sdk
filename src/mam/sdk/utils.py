import json


def validateJSON(json_payload):
    try:
        payload = json.loads(json_payload)
    except ValueError as err:
        return False
    return payload
