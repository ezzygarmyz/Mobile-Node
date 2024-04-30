import os
import json
import requests

def get_t_addresses(config_path):
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
                "method": "listaddressgroupings",
                "params": [],
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
            
            
def get_z_addresses(config_path):
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
                "method": "z_listaddresses",
                "params": [],
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
