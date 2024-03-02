import toga
from toga.colors import rgb
from toga.style.pack import Pack, COLUMN
import requests
import json
import os
import operator

class TransactionsBox(toga.Box):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = None
    
    def set_app(self, app):
        self.app = app

        transactions_data = self.get_transactions_list()
        if transactions_data:
            result_data = transactions_data["result"]
            sorted_transactions = sorted(
                result_data,
                key=operator.itemgetter('timereceived'),
                reverse=True
            )
            for data in sorted_transactions: 
                address = data["address"]
                category = data["category"]
                amount = data["amount"]
                if category == "send":
                    text = "SEND"
                    text_style = Pack(
                        color=rgb(255, 0, 0),
                        font_size="8",
                        font_family="monospace",
                        text_align="right",
                        padding_right=5
                    )
                else:
                    text = "RECEIVE"
                    text_style = Pack(
                        color=rgb(9, 236, 16),
                        font_size="8",
                        font_family="monospace",
                        text_align="right",
                        padding_right=5
                    )
                
                self.address_label = toga.Label(
                    f"{address}",
                    style=Pack(
                        color=rgb(240, 248, 255),
                        font_size="11",
                        font_family="monospace",
                        text_align="center",
                        padding_top=5
                    )
                )
                self.category_label = toga.Label(
                    f"{text}",
                    style=text_style
                )
                self.amount_label = toga.Label(
                    f"{amount} BTCZ",
                    style=Pack(
                        color=rgb(235, 186, 6),
                        font_size="9",
                        font_family="monospace",
                        text_align="left",
                        padding_left=5
                    )
                )
                
                self.transactions_list_box = toga.Box(
                    children=[
                        self.address_label,
                        self.category_label,
                        self.amount_label
                    ],
                    style=Pack(
                    direction=COLUMN,
                    background_color=rgb(60, 60, 60),
                    padding=5
                    )
                )
                self.add(self.transactions_list_box)
        else:
            self.no_transactions_label = toga.Label(
                f"You don't have any transactions yet",
                style=Pack(
                    color=rgb(240, 248, 255),
                    font_size="11",
                    font_family="monospace",
                    text_align="center",
                    padding=(10, 5, 10, 5)
                )
            )
            self.transactions_list_box = toga.Box(
                children=[
                    self.no_transactions_label
                ],
                style=Pack(
                    direction=COLUMN,
                    background_color=rgb(60, 60, 60),
                    padding=(20, 5, 0, 5)
                )
            )
            self.add(self.transactions_list_box)
        
        
    def get_transactions_list(self):
        config_path = self.app.paths.config / 'config.json'
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
                    "id": "0",
                    "method": "listtransactions",
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
        
                    return data
                
        else:
            return