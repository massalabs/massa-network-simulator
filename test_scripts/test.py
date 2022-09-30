import json
import requests
from typing import List

def get_current_period():
    headers = {'Content-type': 'application/json'}
    payload = json.dumps({
        "jsonrpc": "2.0",
        "method": "get_status",
        "id": 0,
        "params": []
    })
    response = requests.post("http://localhost:33033/", data=payload, headers=headers)
    return response.json()
print(get_current_period())

def send_tx_list(tx_list):
    headers = {'Content-type': 'application/json'}
    payload = json.dumps({
        "jsonrpc": "2.0",
        "method": "get_addresses",
        "id": 0,
        "params": [tx_list]
    })
    return requests.post('http://localhost:33037/', data=payload, headers=headers)

def get_balances(addresses):
    headers = {'Content-type': 'application/json'}
    payload = json.dumps({
        "jsonrpc": "2.0",
        "method": "get_addresses",
        "id": 0,
        "params": [addresses]
    })
    response = requests.post("http://localhost:33035/", data=payload, headers=headers)
    return response.json()

def get_operations(ids):
    headers = {'Content-type': 'application/json'}
    payload = json.dumps({
        "jsonrpc": "2.0",
        "method": "get_operations",
        "id": 0,
        "params": [ids]
    })
    response = requests.post("http://localhost:33033/", data=payload, headers=headers)
    return response.json()
print(get_operations(["2pdpJCzqD287LHdABaEhFTC2jK36qjoG4Q2PsFvg9sodKb46n7"]))
#print(get_balances(["A12Gw8CZvASAkMxM5qZRwgwajDoLDsSZi6BpNPTnjyTRiMawe2Gc"]))

def get_block(block_id):
    headers = {'Content-type': 'application/json'}
    payload = json.dumps({
        "jsonrpc": "2.0",
        "method": "get_block",
        "id": 0,
        "params": [block_id]
    })
    response = requests.post("http://localhost:33033/", data=payload, headers=headers)
    return response.json()

print(get_block("cSM1G54iswwCgKnrafFNgeA5ueFH16jpv1VRPjAQKx1xU2Z8z"))

def get_endorsements(endorsement_ids: List[str], url="http://localhost:33033/"):
    headers = {'Content-type': 'application/json'}
    payload = json.dumps({
        "jsonrpc": "2.0",
        "method": "get_endorsements",
        "id": 0,
        "params": [endorsement_ids]
    })
    response = requests.post(url, data=payload, headers=headers)
    return response.json()


def get_cliques(address):
    headers = {'Content-type': 'application/json'}
    payload = json.dumps({
        "jsonrpc": "2.0",
        "method": "get_cliques",
        "id": 0,
        "params": []
    })
    response = requests.post(address, data=payload, headers=headers)
    return response.json()
# a = get_cliques("http://localhost:33032/")["result"][0]["block_ids"]
# a.sort()
# print(a)
# b = get_cliques("http://localhost:33036/")["result"][0]["block_ids"]
# b.sort()
# print(b)
