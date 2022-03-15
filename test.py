import json
import requests

def get_current_period():
    headers = {'Content-type': 'application/json'}
    payload = json.dumps({
        "jsonrpc": "2.0",
        "method": "get_status",
        "id": 0,
        "params": []
    })
    response = requests.post("http://localhost:33037/", data=payload, headers=headers)
    return response.json()['result']['last_slot']['period']
print(get_current_period())