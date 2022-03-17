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

def send_tx_list():
    headers = {'Content-type': 'application/json'}
    payload = json.dumps({
        "jsonrpc": "2.0",
        "method": "send_operations",
        "id": 0,
        "params": [[{'content': {'op': {'Transaction': {'recipient_address': '1RnyG7tQNbvErdmTeLc4TEth3rPfPTHZy5kuu6u2XsyFS9ta5', 'amount': '10000.000000000'}}, 'sender_public_key': '5Zk6UFsghwqjaGRMG6abZjkoGjoZ5bU1H91UWeVqpU7XwjVcEo', 'fee': '0.000000000', 'expire_period': 8}, 'signature': '4f41goakJbP3LZbqp2SMQf2MoBMwRWi8N4iBtnZz21FHpZVkeZs7SWNeQtbLmDdUoCyHTXoM7qa1nh7WeNY1QFAbBMPrT'}, {'content': {'op': {'Transaction': {'recipient_address': '5qvZFCymYnuLMWnaFcnRw6NKzfhGEV6jGEjFFpEQV77kT84Y5', 'amount': '10000.000000000'}}, 'sender_public_key': '5Zk6UFsghwqjaGRMG6abZjkoGjoZ5bU1H91UWeVqpU7XwjVcEo', 'fee': '0.000000000', 'expire_period': 8}, 'signature': 'HJrLBvcVUqXa9vwF17P9n18Y9ZtQTL554Gvw6bzExmdtUZzHFkR4LyGJcdotQfCMeZsNwgPxEwRxp3AH2Fiz1siZueK6t'}, {'content': {'op': {'Transaction': {'recipient_address': '8bELvnmNpVGQbdm2zdKJWF4q6UhGpYWGhFqeGLCR6jq1fvKBi', 'amount': '10000.000000000'}}, 'sender_public_key': '5Zk6UFsghwqjaGRMG6abZjkoGjoZ5bU1H91UWeVqpU7XwjVcEo', 'fee': '0.000000000', 'expire_period': 8}, 'signature': 'SUbgScTyiVw8B8Xeu7yosEP5c959dqX3hKsWuBL5ZnKSwxXFmnprhEcJy6R8fMv4aqRWdo7koACpCbrBMoKfgY3CPAYwf'}, {'content': {'op': {'Transaction': {'recipient_address': 'ErTa2FfwxU96rYbT8Fu5s443LhJ2j2i9vobopAbZfeCRbPjW4', 'amount': '10000.000000000'}}, 'sender_public_key': '5Zk6UFsghwqjaGRMG6abZjkoGjoZ5bU1H91UWeVqpU7XwjVcEo', 'fee': '0.000000000', 'expire_period': 8}, 'signature': 'EuAvq77xqfMuQBJu3qLUkq39LFECQBuNmSWFVpnvtRvzUhpfyrZFBzKRR1HbmiDMHB7HXW2fCobU9VVTG2nGtHUDCB541'}, {'content': {'op': {'Transaction': {'recipient_address': 'HqADztYxrD95RgxLFESA1avTZdEoK4nEByx2qp4qzpkN4d8Uy', 'amount': '10000.000000000'}}, 'sender_public_key': '5Zk6UFsghwqjaGRMG6abZjkoGjoZ5bU1H91UWeVqpU7XwjVcEo', 'fee': '0.000000000', 'expire_period': 8}, 'signature': '2a4W1Skqw3eJVT4DLh5qpr2prvmWGMkmw6YPmuMudV7qNto1wKYRFwuF9EPJoQ5Y2n75UyPGYVXYqRqL9NYLr5x59aorx'}, {'content': {'op': {'Transaction': {'recipient_address': 'MNTvMdNtVawdfjyJRD3k4JEPhyX5YDG3V1PF6di7u6K6pxAAJ', 'amount': '10000.000000000'}}, 'sender_public_key': '5Zk6UFsghwqjaGRMG6abZjkoGjoZ5bU1H91UWeVqpU7XwjVcEo', 'fee': '0.000000000', 'expire_period': 8}, 'signature': 'EAP4SfR4796AZs4fu1czMYjpu5KDuQRAhKpwoCKsTpyXjVh62CccyTEmY8PiQ2J6oNSTMNwTTX688rPoUPc9i1ZZGj3MK'}, {'content': {'op': {'Transaction': {'recipient_address': 'R3kPNxGaeuZyTuWnyNke3XbcdBomhpU2wRMBL3Uc6upoe4dtn', 'amount': '10000.000000000'}}, 'sender_public_key': '5Zk6UFsghwqjaGRMG6abZjkoGjoZ5bU1H91UWeVqpU7XwjVcEo', 'fee': '0.000000000', 'expire_period': 8}, 'signature': 'CCNiiAZm38733Mnha115qF4ZymY957hxjczVGVMPeheX8HGCLbgTP4JUXt4YtV4f1Yr6sTDrhEZUWjG1pYxfMjFXHKb5K'}, {'content': {'op': {'Transaction': {'recipient_address': 'Trsfo9GiWMY6ZN3V9AC4Bib1FvkCSDsEjBhiiHkXN3mYZJeCY', 'amount': '10000.000000000'}}, 'sender_public_key': '5Zk6UFsghwqjaGRMG6abZjkoGjoZ5bU1H91UWeVqpU7XwjVcEo', 'fee': '0.000000000', 'expire_period': 8}, 'signature': 'WQfMWK4rbxLcMLj11iW6wV7uRNRXu1bHjvcrFb5hpQEvBx336fbNDzgc9deJKrRVcy18EV6PeadPNcFmLgnCHBwX1Kdg4'}, {'content': {'op': {'Transaction': {'recipient_address': 'X1i3FzAnQr5vjEodjQpnS7haP2uBhXSagfnY4Eg9TjA2LYBEs', 'amount': '10000.000000000'}}, 'sender_public_key': '5Zk6UFsghwqjaGRMG6abZjkoGjoZ5bU1H91UWeVqpU7XwjVcEo', 'fee': '0.000000000', 'expire_period': 8}, 'signature': 'H149AfAZr8vxDrxTeqnS9GfbJogzCpQZHHy12i2PLxAf8yvu8LLm7XnQ1VA9UdHTahsUvQxgAGMZvQQjQa86fxSZnQsk3'}, {'content': {'op': {'Transaction': {'recipient_address': 'ZAJjT4dvsqZ65e52c3Dprg5g4eREhjXQSEtPaUgtrfD3ZWugf', 'amount': '10000.000000000'}}, 'sender_public_key': '5Zk6UFsghwqjaGRMG6abZjkoGjoZ5bU1H91UWeVqpU7XwjVcEo', 'fee': '0.000000000', 'expire_period': 8}, 'signature': 'By6nuQwei4cxAEb176vJ7g29gYfwYiYNBdvohiVsV5zr37Rbu92h1oWChKEBEF32JK3uNDn13CAqYQf4SxVB6ioEcrKNk'}, {'content': {'op': {'Transaction': {'recipient_address': 'fLc4WHvyR7jRux9VmUzCcG1EPn1bntQ8PZr1qD3bwWfJUjATN', 'amount': '10000.000000000'}}, 'sender_public_key': '5Zk6UFsghwqjaGRMG6abZjkoGjoZ5bU1H91UWeVqpU7XwjVcEo', 'fee': '0.000000000', 'expire_period': 8}, 'signature': 'CQrNYx6PMS7hV8DQxaVsrXQi6LkbB9ZGdm3ZBosuaFu6ZXULv4UNx1c1pT8yuuLFFJQPHmVRcdtXYHnqBhRrWBoErNkvi'}, {'content': {'op': {'Transaction': {'recipient_address': 'iEbniXSPLa2ckNniSmRecD15WfWFAk8uX7uwNgXVZ9DxA2RBu', 'amount': '10000.000000000'}}, 'sender_public_key': '5Zk6UFsghwqjaGRMG6abZjkoGjoZ5bU1H91UWeVqpU7XwjVcEo', 'fee': '0.000000000', 'expire_period': 8}, 'signature': 'QMdv2rsVExrweDNqsb3U2PxiBHayqjrUAqzHMKv9B3dkfu3vMhC7yBU3BzU8LSeqd1Fmhq4pZhEnZxQN8rAbRFTdzu5wt'}, {'content': {'op': {'Transaction': {'recipient_address': 'jvVMjYXVbLY1Fpq6hpta7HAHGaAKm9ZEjTTLyJuPf5MBSPnDJ', 'amount': '10000.000000000'}}, 'sender_public_key': '5Zk6UFsghwqjaGRMG6abZjkoGjoZ5bU1H91UWeVqpU7XwjVcEo', 'fee': '0.000000000', 'expire_period': 8}, 'signature': 'DgwDyqhDq6bsrnSB8ppcFaE43f7gqqjCFdz2xkWT6iyvPR9Q9HFgRA2oSNGB9s51rsENTWqDibMNSTwMkuGFAC31rxGYu'}, {'content': {'op': {'Transaction': {'recipient_address': 'qhuicra96FZ2phytipah2E24XK4sJE4iyJfMzCUQgEVLm19dq', 'amount': '10000.000000000'}}, 'sender_public_key': '5Zk6UFsghwqjaGRMG6abZjkoGjoZ5bU1H91UWeVqpU7XwjVcEo', 'fee': '0.000000000', 'expire_period': 8}, 'signature': '7VuCwN3zarfGPtsmEF7iUms1Ad5oWP1VCRpsT4k24hGVLyasdq7dCMVGRLCUKntRt6ahjhtUqLCWuoVpKfYnm1FkRGi99'}, {'content': {'op': {'Transaction': {'recipient_address': 'uiSMA8fqYzBcVZSpJgWXa26QMPiVhq4LsU9dSGgiCR4JBVQy2', 'amount': '10000.000000000'}}, 'sender_public_key': '5Zk6UFsghwqjaGRMG6abZjkoGjoZ5bU1H91UWeVqpU7XwjVcEo', 'fee': '0.000000000', 'expire_period': 8}, 'signature': '74MV5k441kbMMSPKszNvdHFA4wq4Ast4dvf8KqQkfrTB8pcqXSkRNHvH69xYCfwj1DNmD4dLjhV7AxoNucyBhHsiE1dRs'}, {'content': {'op': {'Transaction': {'recipient_address': 'vmzEpq2nRiFPsg33e68znP52o2pKfM8iXRhRcH9XSzZWjvW2F', 'amount': '10000.000000000'}}, 'sender_public_key': '5Zk6UFsghwqjaGRMG6abZjkoGjoZ5bU1H91UWeVqpU7XwjVcEo', 'fee': '0.000000000', 'expire_period': 8}, 'signature': 'DuqBhDtBudxtpfnFHNs65wWsuVjAVzmAUjdfRarmYj1qLrURUMoUEjxRhgeMUcaNHdwypg98LyWmW2DsZV54pfMyj1tVY'}, {'content': {'op': {'Transaction': {'recipient_address': '21hecismPPs5ZU6qeNAmiStqTDM9PFfxGKzsBuZEPxWdq9cEfk', 'amount': '10000.000000000'}}, 'sender_public_key': '5Zk6UFsghwqjaGRMG6abZjkoGjoZ5bU1H91UWeVqpU7XwjVcEo', 'fee': '0.000000000', 'expire_period': 8}, 'signature': '8NNGkuPTSCYv6S51Npa6Ss3KtjarDQbJXLiihsM5X59J8VCD5P26HD1MeGUL28NyaaTtTNUQ9q59enUQEFcgyGF6QrJZD'}, {'content': {'op': {'Transaction': {'recipient_address': '25Y55dkae9RWvhfyfLFPde3e52gLJ57aV1RxABDba7bWYXMLjX', 'amount': '10000.000000000'}}, 'sender_public_key': '5Zk6UFsghwqjaGRMG6abZjkoGjoZ5bU1H91UWeVqpU7XwjVcEo', 'fee': '0.000000000', 'expire_period': 8}, 'signature': 'QCgjJp3oL7u6oJt3Gbs8d55RrtWoEFpVZ42KtshFGZCBpJNKttaeJJU9nArxip73hj6Lfw1mKZijN9K1XcVx9eyb3Kejd'}, {'content': {'op': {'Transaction': {'recipient_address': '28UaBpZRe7NjGCqnVnSU5d4whk29g4AFTFbhfuqigKL6QagbEC', 'amount': '10000.000000000'}}, 'sender_public_key': '5Zk6UFsghwqjaGRMG6abZjkoGjoZ5bU1H91UWeVqpU7XwjVcEo', 'fee': '0.000000000', 'expire_period': 8}, 'signature': 'ABSYi2DxkKizfhUW9D8axKUfWE4nWsvrsJMdFX1CrcgezEawg7Mh9hezPt74w8QCYvhLfC5tizqSKD8WDnS9uajgdmqFb'}, {'content': {'op': {'Transaction': {'recipient_address': '2DMDFPdCFAx14oqBsubB4zojoTYYTCsWSpjkTQPev7UToyGNvf', 'amount': '10000.000000000'}}, 'sender_public_key': '5Zk6UFsghwqjaGRMG6abZjkoGjoZ5bU1H91UWeVqpU7XwjVcEo', 'fee': '0.000000000', 'expire_period': 8}, 'signature': 'Ax6KswBe91LcQLTxfVkxWHfH1GDX73zjYjGadwCxv5uebjEY9fBb3Yf9a8mS5YRDDwSrWKgVKRCxVL5UfwDPG9xAffswL'}, {'content': {'op': {'Transaction': {'recipient_address': '2ELewbpWyCNmwXmknc5moQ1ueU6TcUf1bRc8KfyjJqfT3DVbkx', 'amount': '10000.000000000'}}, 'sender_public_key': '5Zk6UFsghwqjaGRMG6abZjkoGjoZ5bU1H91UWeVqpU7XwjVcEo', 'fee': '0.000000000', 'expire_period': 8}, 'signature': 'JHz6HC8VL17ZKszUE5jV7Yh2gd4j4WLHdnaUcnBkKTPGhgP3zYU82XZqEUqnUd5qRqB1A3SbWe1J1sTvUNHBR3PcgoMN5'}, {'content': {'op': {'Transaction': {'recipient_address': '2Kn9ZsN7N8EqAMhRssatTj3AhRcoZD22iK9JoPw9QSjFgqZBCX', 'amount': '10000.000000000'}}, 'sender_public_key': '5Zk6UFsghwqjaGRMG6abZjkoGjoZ5bU1H91UWeVqpU7XwjVcEo', 'fee': '0.000000000', 'expire_period': 8}, 'signature': 'EpJp2ZaiHiGojqC9A2xsaXM9AfJjcYPgCjoKKqvyQRZ66QGZcvNnBRPa1dj4ksJtqoNNMKGtLCsHMFDiAjXpVGKCpHLGn'}, {'content': {'op': {'Transaction': {'recipient_address': '2NUEbpUXdokhQ96xfC1w9UYD9Tv5atRHBkc5fie1wfVy4qS38k', 'amount': '10000.000000000'}}, 'sender_public_key': '5Zk6UFsghwqjaGRMG6abZjkoGjoZ5bU1H91UWeVqpU7XwjVcEo', 'fee': '0.000000000', 'expire_period': 8}, 'signature': 'FY4ej62LEsWofvqdfQDYCX9n5y9BrYX2KgZRHZZdbpqhb3ULApTGVJmfBDAPsG8jAuxq3ZrcYQKyRrVAXYVD7hMmfZv8L'}, {'content': {'op': {'Transaction': {'recipient_address': '2RfcUaPFFdiPptUecQQrfHTZTURUkj9rLSSSVsXH414NPjUbe3', 'amount': '10000.000000000'}}, 'sender_public_key': '5Zk6UFsghwqjaGRMG6abZjkoGjoZ5bU1H91UWeVqpU7XwjVcEo', 'fee': '0.000000000', 'expire_period': 8}, 'signature': 'LY5B1vRMD9FGv5rBDdkN8u83o17NUPE4VgMCQEDQDn5q6xRypNSzkppPYFJgzS4QsnMnESF2QSaSPVndnktFsZ9STcdqV'}, {'content': {'op': {'Transaction': {'recipient_address': '2UCtDceUm3HX6ELhnZmUxuLQ32tbApHX6wtLmW76tZpcUaMvHX', 'amount': '10000.000000000'}}, 'sender_public_key': '5Zk6UFsghwqjaGRMG6abZjkoGjoZ5bU1H91UWeVqpU7XwjVcEo', 'fee': '0.000000000', 'expire_period': 8}, 'signature': 'RD754uzFQoxU3ji2QCN4ZuhXSR34EqHPVSVestPWV8nMukLDK8DpBKr9VbER4bfhubxDvkvqZ979cg1oYktYeNatcofP'}, {'content': {'op': {'Transaction': {'recipient_address': '2Yq5KZnLXoaAH3BrtPgeqBhjiyCc1XtS2TtxBjoZ2fricAG3fN', 'amount': '10000.000000000'}}, 'sender_public_key': '5Zk6UFsghwqjaGRMG6abZjkoGjoZ5bU1H91UWeVqpU7XwjVcEo', 'fee': '0.000000000', 'expire_period': 8}, 'signature': 'BMpyXYRZPBEd11nzg1xWaPvamsgsgvaKrVfvBDdrSgsyhVHsyh5n1z8MDzYqfoeJCchXRwjm9QB4hcXhEou1PdMW93G8M'}, {'content': {'op': {'Transaction': {'recipient_address': '2aoUHM3xhavXMRpWmiaK68m5NYCGWd5kt5xKom6KZxPaaY4E9q', 'amount': '10000.000000000'}}, 'sender_public_key': '5Zk6UFsghwqjaGRMG6abZjkoGjoZ5bU1H91UWeVqpU7XwjVcEo', 'fee': '0.000000000', 'expire_period': 8}, 'signature': 'M8kJg8K1jpcZMpzsBL3wGX8j4ihn48v7VDscbHhken8iUFL4sUYaCEEiAz4d4vCwKMk3RsmhbBtQcAVdzAAjRMVysvA7h'}, {'content': {'op': {'Transaction': {'recipient_address': '2eDAG1czh8XKTKqhLyDKYCMVXdUGxN51AwSiiPHrqz4osfjfdV', 'amount': '10000.000000000'}}, 'sender_public_key': '5Zk6UFsghwqjaGRMG6abZjkoGjoZ5bU1H91UWeVqpU7XwjVcEo', 'fee': '0.000000000', 'expire_period': 8}, 'signature': '2h5rYkP6uGYSoQ9K6Hnze3MghY4rREHcKUmkV7kq1n8mUhmGK28kRKdgVpkd1oT21YhHKxuSB5NP956NVPgQ8sCn8qJvb'}, {'content': {'op': {'Transaction': {'recipient_address': '2hj5CjarK7zdNmz1cHbD7VizMYmLM8R1PTbWt3u7x6WGkNLzjw', 'amount': '10000.000000000'}}, 'sender_public_key': '5Zk6UFsghwqjaGRMG6abZjkoGjoZ5bU1H91UWeVqpU7XwjVcEo', 'fee': '0.000000000', 'expire_period': 8}, 'signature': 'VgcxgbW15E3mgZxaWWzPF5CEQXAL2RRrbj5v3FfBamqFaHBGbauYvMkDJb4y8oyQsp3m22iMMa8vnQzrbZ8T2xs5meQPw'}, {'content': {'op': {'Transaction': {'recipient_address': '2o3jwc9rXuED7yH1Ra2LViE9oTqJFVBTBAVyoBWsgw4NFqqCiJ', 'amount': '10000.000000000'}}, 'sender_public_key': '5Zk6UFsghwqjaGRMG6abZjkoGjoZ5bU1H91UWeVqpU7XwjVcEo', 'fee': '0.000000000', 'expire_period': 8}, 'signature': '7uUXvpVxJBUmAL62y4wqEahFtnGbjet841S3p51NvzMGVvBnUZdR5vu19mGQGPpHwcHCMzdAGzcXdTntCbtrDKYoz14Ph'}, {'content': {'op': {'Transaction': {'recipient_address': '2qHghDVkUXpc6AycFNN7w9vv4Ky9SRRFEGAj5r5QUBAmCsgRRr', 'amount': '10000.000000000'}}, 'sender_public_key': '5Zk6UFsghwqjaGRMG6abZjkoGjoZ5bU1H91UWeVqpU7XwjVcEo', 'fee': '0.000000000', 'expire_period': 8}, 'signature': 'ZVLUSw6iM4ZGN1JHxB6Xgu1ZSavCPMRpHbXkbkQzPMKjMscNntewdvstuogt7Rz8KPxvVec5UcNciuQQ7XBVb9GZgFe8k'}, {'content': {'op': {'Transaction': {'recipient_address': '2tRV7tduN5p8VBVS67zua64wT9843GGvWpQPaLMuAZHBdQ74RP', 'amount': '10000.000000000'}}, 'sender_public_key': '5Zk6UFsghwqjaGRMG6abZjkoGjoZ5bU1H91UWeVqpU7XwjVcEo', 'fee': '0.000000000', 'expire_period': 8}, 'signature': '8XpyWyms93SqM54ovJwRBd2eQrDMCohXUahqJM4Ap8BovRUVTa77jLWDbkozQodtH8dhW15He33q3XFUp61hjdwMqUpuC'}]]
    })
    return requests.post('http://localhost:33035/', data=payload, headers=headers)
print(send_tx_list().json())

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
    response = requests.post("http://localhost:33035/", data=payload, headers=headers)
    return response.json()

#print(get_block("P6RuE4xXvaZdthHbnjsCukX1sFQ4AY1Y9AMyksZ3xQgcjyiPV"))