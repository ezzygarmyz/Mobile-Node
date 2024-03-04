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
            url = f"http://{rpc_user}:{rpc_password}@{rpc_host}:{rpc_port}"

            headers = {"content-type": "application/json"}
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
