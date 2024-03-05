import toga
from toga.colors import rgb
from toga.style.pack import Pack, COLUMN
import requests
import json
import os


class MainBalanceBox(toga.Box):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = None
    
    def set_app(self, app):
        self.app = app

        total, transparent, private = self.get_total_balance()
        
        self.balance_box = toga.Box(
            children=[
                toga.Label(
                    f"Total Balance",
                    style=Pack(
                        text_align="center",
                        font_size="16",
                        font_family="monospace",
                        color=rgb(240, 248, 255),
                        padding=(60, 0, 0, 0),
                        font_weight="bold"
                    )
                ),
                
                toga.Label(
                    f"{total} BTCZ",
                    style=Pack(
                        text_align="center",
                        font_size="22",
                        font_family="monospace",
                        color=rgb(240, 248, 255),
                        padding=(10, 0, 0, 0),
                        font_weight="bold"
                    )
                ),
                
                toga.Label(
                    f"T : {transparent} BTCZ",
                    style=Pack(text_align="center",
                    font_size="10",
                    font_family="monospace",
                    color=rgb(240, 248, 255),
                    padding=(15, 0, 0, 0))),
                
                toga.Label(
                    f"Z : {private} BTCZ",
                    style=Pack(text_align="center",
                    font_size="10",
                    font_family="monospace",
                    color=rgb(0, 179, 241),
                    padding=(2, 0, 50, 0))),
            ],
            style=Pack(
                direction=COLUMN,
                background_color=rgb(60, 60, 60),
                padding=5)
        )
        
        self.balances_box_devider = toga.Box(
            children=[
                toga.Label(
                    f"[ Blockchain Info ]",
                    style=Pack(
                        text_align="center",
                        font_size="10",
                        font_family="monospace",
                        color=rgb(240, 248, 255))),
                
                toga.Divider(
                    direction="HORIZONTAL",
                    style=Pack(padding=(1, 5, 1, 5)))
            ],
            style=Pack(
                direction=COLUMN,
                background_color=rgb(60, 60, 60),
                padding=5)
        )
        
        blocks, header, difficulty, disk_size, commitments = self.get_blockchain_info()
        
        self.blockchain_info = toga.Box(
            children=[
                toga.Label(
                    f"Blocks : {blocks}",
                    style=Pack(font_size="10",
                    font_family="monospace",
                    color=rgb(240, 248, 255),
                    padding=(10, 0, 5, 10))),
                
                toga.Label(
                    f"Headers : {header}", 
                    style=Pack(font_size="10",
                    font_family="monospace",
                    color=rgb(240, 248, 255),
                    padding=(0, 0, 5, 10))),
                
                toga.Label(
                    f"Difficulty : {float(difficulty):.2f}",
                    style=Pack(font_size="10",
                    font_family="monospace",
                    color=rgb(240, 248, 255),
                    padding=(0, 0, 5, 10))),
                
                toga.Label(
                    f"Commitments : {commitments}",
                    style=Pack(font_size="10",
                    font_family="monospace",
                    color=rgb(240, 248, 255),
                    padding=(0, 0, 5, 10))),
                
                toga.Label(
                    f"Size On Disk : {float(disk_size):.1f} GB",
                    style=Pack(
                        font_size="10",
                        font_family="monospace",
                        color=rgb(240, 248, 255),
                        padding=(0, 0, 10, 10)
                        )
                    ),
            ],
            style=Pack(
                direction=COLUMN,
                background_color=rgb(60, 60, 60),
                padding=5
            )
        )
        
        self.add(
            self.balance_box,
            self.balances_box_devider,
            self.blockchain_info
        )

    def format_total_balance(self, total):
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

    def get_total_balance(self):
        config_path = self.app.paths.config / 'config.json'

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
                    total = self.format_total_balance(
                        float(data_result["total"])
                    )
                    transparent = self.format_total_balance(
                        float(data_result["transparent"])
                    )
                    private = self.format_total_balance(
                        float(data_result["private"])
                    )
        else:
            total = "0.00"
            transparent = "0.00"
            private = "0.00"
        return total, transparent, private
        
        
    def get_blockchain_info(self):
        config_path = self.app.paths.config / 'config.json'
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
                    blocks = data_result["blocks"]
                    header = data_result["headers"]
                    difficulty = data_result["difficulty"]
                    disk_size = data_result["size_on_disk"]
                    disk_size_gb = disk_size / (1024**3)
                    commitments = data_result["commitments"]
        else:
            blocks = "0"
            header = "0"
            difficulty = "0"
            disk_size_gb = "0"
            commitments = "0"
        return blocks, header, difficulty, disk_size_gb, commitments
