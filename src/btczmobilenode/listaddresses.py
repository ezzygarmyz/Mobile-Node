import toga
from toga.colors import rgb
from toga.style.pack import Pack, COLUMN, ROW, CENTER
import requests
import json
import os
import operator
from datetime import datetime, timezone

from btczmobilenode.listtransactions import get_transactions_list, get_transaction

class TransactionsBox(toga.Box):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = None
    
    def set_app(self, app):
        self.app = app
        config_path = self.app.paths.config / 'config.json'

        transactions_data = get_transactions_list(config_path)
        if transactions_data:
            result_data = transactions_data["result"]
            sorted_transactions = sorted(
                result_data,
                key=operator.itemgetter('timereceived'),
                reverse=True
            )
            for data in sorted_transactions: 
                address = data.get("address", "Shielded")
                category = data["category"]
                amount = data["amount"]
                timereceived = data["timereceived"]
                formatted_date_time = datetime.fromtimestamp(timereceived, tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
                txid = data["txid"]
                    
                if category == "send":
                    text = "SEND"
                    text_style = Pack(
                        color=rgb(255, 0, 0),
                        font_size="8",
                        font_family="monospace",
                        text_align="center",
                        font_weight="bold",
                        padding=5
                    )
                else:
                    text = "RECEIVE"
                    text_style = Pack(
                        color=rgb(9, 236, 16),
                        font_size="8",
                        font_family="monospace",
                        text_align="center",
                        font_weight="bold",
                        padding=5
                    )
                
                self.address_label = toga.Label(
                    f"{address}",
                    style=Pack(
                        color=rgb(240, 248, 255),
                        font_size="11",
                        font_family="monospace",
                        text_align="center",
                        padding=5
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
                        font_size="10",
                        font_family="monospace",
                        text_align="center",
                        padding=5,
                        font_weight="bold"
                    )
                )
                
                self.amount_box = toga.Box(
                    children=[
                        self.amount_label
                    ],
                    style=Pack(
                        padding=5,
                        flex=1
                    )
                )
                
                self.category_box = toga.Box(
                    children=[
                        self.category_label
                    ],
                    style=Pack(
                        padding=5
                    )
                )
                
                
                self.transaction_info_box = toga.Box(
                    children=[
                        self.amount_box,
                        self.category_box
                    ],
                    style=Pack(
                        padding=5,
                        direction=ROW,
                        background_color=rgb(70, 70, 70),
                    )
                )
                
                self.time_received_label = toga.Label(
                    f"{formatted_date_time}",
                    style=Pack(
                        text_align="center",
                        font_size="10",
                        font_family="monospace",
                        padding=5,
                        color=rgb(240, 248, 255)
                    )
                )
                
                self.transaction_button = toga.Button(
                    "More Info",
                    style=Pack(
                        color=rgb(240, 248, 255),
                        background_color=rgb(60, 60, 60),
                        font_family="monospace",
                    ),
                    on_press=lambda widget, txid=txid: self.transaction_window(txid)
                )
                
                self.transaction_button_box = toga.Box(
                    children=[
                        self.transaction_button
                    ],
                    style=Pack(
                        background_color=rgb(70, 70, 70),
                        direction=COLUMN,
                    )
                )
                
                self.transactions_list_box = toga.Box(
                    children=[
                        self.address_label,
                        self.transaction_info_box,
                        self.time_received_label,
                        self.transaction_button_box
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
        
        
    def transaction_window(self, txid):
        config_path = self.app.paths.config / 'config.json'
        data_info = get_transaction(config_path, txid)
        if data_info:
            confirmations = data_info["confirmations"]
            blockhash = data_info["blockhash"]
            blockindex = data_info["blockindex"]
            expiryheight = data_info["expiryheight"]
            txid = data_info["txid"]
            self.app.main_window.info_dialog(
                "Transaction Info :",
                f"- Confirmations : {confirmations}\n- Blockhash : {blockhash}\n- Blockindex : {blockindex}\n- Expiryheight : {expiryheight}\n- Txid : {txid}"
            )
