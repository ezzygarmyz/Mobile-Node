import requests
import json
import os


def format_total_balance(total):
        formatted_total = '{:.8f}'.format(total)  
        parts = formatted_total.split('.')  
        integer_part = parts[0]
        decimal_part = parts[1] 

        if len(integer_part) > 4:
            digits_to_remove = len(integer_part) - 4
            formatted_decimal = decimal_part[:-digits_to_remove]
        else:
            formatted_decimal = decimal_part

        formatted_balance = integer_part + '.' + formatted_decimal
        return formatted_balance


def get_total_balance(config_path):
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
                "method": "z_gettotalbalance",
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
                total = format_total_balance(
                    float(data_result["total"])
                )
                transparent = format_total_balance(
                    float(data_result["transparent"])
                )
                private = format_total_balance(
                    float(data_result["private"])
                )
    else:
        total = "0.00"
        transparent = "0.00"
        private = "0.00"
    return total, transparent, private


def get_blockchain_info(config_path):
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
                "method": "getblockchaininfo",
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
                chain = data_result["chain"]
                blocks = data_result["blocks"]
                header = data_result["headers"]
                bestblock = data_result["bestblockhash"]
                bestblockheight = get_block_height(config_path ,bestblock)
                verificationprogress = data_result["verificationprogress"]
                verificationpercentage = verificationprogress * 100
                difficulty = data_result["difficulty"]
                disk_size = data_result["size_on_disk"]
                disk_size_gb = disk_size / (1024**3)
                commitments = data_result["commitments"]
    else:
        chain = "None"
        blocks = "0"
        header = "0"
        bestblockheight = "0"
        verificationpercentage = "0.00"
        difficulty = "0.00"
        disk_size_gb = "0.00"
        commitments = "0"
    return chain, blocks, header, bestblockheight, verificationpercentage, difficulty, disk_size_gb, commitments


def get_block_height(config_path ,bestblock):
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
                "method": "getblock",
                "params": [f"{bestblock}"],
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
                height = data_result["height"]
                
                return height
            
            
def get_unconfirmedbalance(config_path):
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
                "method": "getunconfirmedbalance",
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
