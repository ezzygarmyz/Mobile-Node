import requests
import json
import os


def new_operation_t(config_path, address, toaddress, amount, tx_fee):
    if os.path.exists(config_path):
        with open(config_path, "r") as config_file:
            config = json.load(config_file)
            rpc_user = config.get("rpcuser")
            rpc_password = config.get("rpcpassword")
            rpc_host = config.get("rpchost")
            rpc_port = config.get("rpcport")
            url = f"http://{rpc_host}:{rpc_port}"

            headers = {"content-type": "text/plain"}
            payload = {
                "jsonrpc": "1.0",
                "id": "curltest",
                "method": "z_sendmany",
                "params": [f"{address}", [{"address": f"{toaddress}", "amount": float(amount)}], 1, float(tx_fee)],
            }
            response = requests.post(
                url,
                data=json.dumps(payload),
                headers=headers,
                auth=(rpc_user, rpc_password),
            )

            if response.status_code == 200:
                data = response.json()
                operation_id = data.get("result")
                
                return operation_id
            
            
def new_operation_z(config_path, address, toaddress, amount, tx_fee):
    if os.path.exists(config_path):
        with open(config_path, "r") as config_file:
            config = json.load(config_file)
            rpc_user = config.get("rpcuser")
            rpc_password = config.get("rpcpassword")
            rpc_host = config.get("rpchost")
            rpc_port = config.get("rpcport")
            url = f"http://{rpc_host}:{rpc_port}"
            
            params = [f"{address}", [{"address": f"{toaddress}", "amount": float(amount)}], 1, float(tx_fee)]

            headers = {"content-type": "text/plain"}
            payload = {
                "jsonrpc": "1.0",
                "id": "curltest",
                "method": "z_sendmany",
                "params": params,
            }
            response = requests.post(
                url,
                data=json.dumps(payload),
                headers=headers,
                auth=(rpc_user, rpc_password),
            )

            if response.status_code == 200:
                data = response.json()
                operation_id = data.get("result")
                
                return operation_id
            
            
def new_operation_z_memo(config_path, address, toaddress, amount, tx_fee, memo):
    if os.path.exists(config_path):
        with open(config_path, "r") as config_file:
            config = json.load(config_file)
            rpc_user = config.get("rpcuser")
            rpc_password = config.get("rpcpassword")
            rpc_host = config.get("rpchost")
            rpc_port = config.get("rpcport")
            url = f"http://{rpc_host}:{rpc_port}"
            memo_hex = memo.encode().hex()
            
            params =  [f"{address}", [{"address": f"{toaddress}", "amount": float(amount), "memo": memo_hex}], 1, float(tx_fee)]

            headers = {"content-type": "text/plain"}
            payload = {
                "jsonrpc": "1.0",
                "id": "curltest",
                "method": "z_sendmany",
                "params": params,
            }
            response = requests.post(
                url,
                data=json.dumps(payload),
                headers=headers,
                auth=(rpc_user, rpc_password),
            )

            if response.status_code == 200:
                data = response.json()
                print(data)
                operation_id = data.get("result")
                
                return operation_id
            

def check_operation_status(config_path, operation_id):
    print(operation_id)
    if os.path.exists(config_path):
        with open(config_path, "r") as config_file:
            config = json.load(config_file)
            rpc_user = config.get("rpcuser")
            rpc_password = config.get("rpcpassword")
            rpc_host = config.get("rpchost")
            rpc_port = config.get("rpcport")
            url = f"http://{rpc_host}:{rpc_port}"

            headers = {"content-type": "text/plain"}
            payload = {
                "jsonrpc": "1.0",
                "id": "curltest",
                "method": "z_getoperationstatus",
                "params": [[f"{operation_id}"]],
            }
            response = requests.post(
                url,
                data=json.dumps(payload),
                headers=headers,
                auth=(rpc_user, rpc_password),
            )

            if response.status_code == 200:
                data = response.json()
                data_result = data["result"]
                
                return data_result