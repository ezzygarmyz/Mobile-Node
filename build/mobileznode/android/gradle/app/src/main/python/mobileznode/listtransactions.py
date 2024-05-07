import requests
import json
import os


def get_transactions_list(config_path):
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
                "method": "listtransactions",
                "params": ["*", 25],
            }
            response = requests.post(
                url,
                data=json.dumps(payload),
                headers=headers,
                auth=(rpc_user, rpc_password),
            )

            if response.status_code == 200:
                data = response.json()
        
                return data
                
    else:
        return
    
    
def get_transaction(config_path, txid):
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
                "method": "gettransaction",
                "params": [f"{txid}"],
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
