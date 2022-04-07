## Run cmd python analyse_operations.py log_file_1 log_file_2 ...

import sys
import json

def parsing(data):
    n_batch_received = 0
    n_batch_received_total = 0
    op_ids_received = {} # dict {op_id: [node_id]}
    n_asked_batches = 0
    n_asked_batches_total = 0
    op_ids_asked = {} # dict {op_id: [node_id]}
    n_op_received_total = 0
    re_ask_count = 0
    buffer_full_count = 0
    tmp = 0
    buffer_len = 0
    depile_count = 0
    send_empty_batch_count = 0
    for line in data:
        # receive batch ids
        if "protocol.protocol_worker.on_network_event.received_operation_batch" in line:
            n_batch_received = n_batch_received + 1
            record = line.split("received_operation_batch:")[1]
            r = json.loads(record)
            tmp = len(r['operation_ids'])
            for op_id in r['operation_ids']:
                n_batch_received_total = n_batch_received_total + 1
                if op_id in op_ids_received:
                    op_ids_received[op_id].append(r['node'])
                else:
                    op_ids_received[op_id]= [r['node']]
        
        # ask operations
        if "node_worker.run_loop. receive Message::AskForOperations:" in line:
            n_asked_batches = n_asked_batches + 1
            record = line.split("receive Message::AskForOperations:")[1]
            r = json.loads(record)
            for op_id in r['operations']:
                n_asked_batches_total = n_asked_batches_total + 1
                if op_id in op_ids_asked:
                    op_ids_asked[op_id].append(r['node'])
                else:
                    op_ids_asked[op_id]= [r['node']]
        
        if "node_worker.run_loop. receive Message::Operations:" in line:
            n_batch_received = n_batch_received + 1
            record = line.split("Message::Operations:")[1]
            r = json.loads(record)
            n_op_received_total = n_op_received_total + len(r['operations'])
        if "re-ask operation" in line:
            re_ask_count += 1
        if "buffer full" in line:
            buffer_full_count += 1
        if "Size of op batch buffer" in line:
            record = line.split("Size of op batch buffer")[1]
            buffer_len = record
        if "depile" in line:
            depile_count += 1
        if "send empty batch" in line:
            send_empty_batch_count += 1
                

    print(f"Received {len(op_ids_received)} operation ids, total op_id*node = {n_batch_received_total}, through {n_batch_received} batches")
    check_received_operations(op_ids_received)
    print(f"Asked {len(op_ids_asked)} operation ids, total op_id*node = {n_asked_batches_total}, in {n_asked_batches} questions")
    check_asked_operations(op_ids_asked)
    print(f"Total operations received: {n_op_received_total}")
    print(f"Total Reask operations total: {re_ask_count}")
    print(f"Total buffer full: {buffer_full_count}")
    print(f"Size of batch: {tmp}")
    print(f"Number of tries to send empty batches {send_empty_batch_count}")
    print(f"Len of the buffer of batches: {buffer_len}")
    print(f"We have removed {depile_count} elements from the buffer of batches")

# Sanity check on received operations
# - op_ids_received: dict {op_id: [node_id]}
def check_received_operations(op_ids_received):
    # verify if received multiple times by the same node
    for key in op_ids_received:
        tmp = []
        for node in op_ids_received[key]:
            if node in tmp:
                assert False, f"Received the operation {key} multiple times from node {node}"
            else:
                tmp.append(node)

# Sanity check on received operations
# - op_ids_received: dict {op_id: [node_id]}
def check_asked_operations(op_ids_asked):
    # verify if received multiple times by the same node
    for key in op_ids_asked:
        tmp = []
        for node in op_ids_asked[key]:
            if node in tmp:
                assert False, f"Ask the operation {key} multiple times to the same node {node}"
            else:
                tmp.append(node)

if __name__ == "__main__":
    for i, arg in enumerate(sys.argv):
        if i > 0:
            print("----------------------------------------")
            print(f"Compute file {arg} to look at operations")
            with open(arg, 'r') as file_data:
                parsing(file_data)
