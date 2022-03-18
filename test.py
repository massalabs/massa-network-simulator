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
    response = requests.post("http://localhost:33036/", data=payload, headers=headers)
    return response.json()['result']['last_slot']['period']
#print(get_current_period())

def send_tx_list(tx_list):
    headers = {'Content-type': 'application/json'}
    payload = json.dumps({
        "jsonrpc": "2.0",
        "method": "get_addresses",
        "id": 0,
        "params": [tx_list]
    })
    return requests.post('http://localhost:33035/', data=payload, headers=headers)

def get_balances(addresses):
    headers = {'Content-type': 'application/json'}
    payload = json.dumps({
        "jsonrpc": "2.0",
        "method": "get_addresses",
        "id": 0,
        "params": [addresses]
    })
    response = requests.post("http://localhost:33036/", data=payload, headers=headers)
    return response.json()

#print(get_balances(["1RnyG7tQNbvErdmTeLc4TEth3rPfPTHZy5kuu6u2XsyFS9ta5"]))

def get_block(block_id):
    headers = {'Content-type': 'application/json'}
    payload = json.dumps({
        "jsonrpc": "2.0",
        "method": "get_block",
        "id": 0,
        "params": [block_id]
    })
    response = requests.post("http://localhost:33036/", data=payload, headers=headers)
    return response.json()

print(get_block("2ffrRJjeQC7t3Jia1tevdkdWCVVvGpxtZ4XZKNSqM4N2QoqZ4c"))