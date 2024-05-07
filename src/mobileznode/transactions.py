import toga
from toga.colors import rgb
from toga.style.pack import Pack, COLUMN, ROW
import operator
from datetime import datetime, timezone

from .listtransactions import get_transactions_list, get_transaction

class TransactionsBox(toga.Box):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = None
    
    def set_app(self, app):
        self.app = app
        
        self.update_button = toga.Button(
            "Update transactions",
            enabled=True,
            on_press=self.update_transactions_list,
            style=Pack(
                font_family="monospace",
            )
        )
        
        self.update_button_box = toga.Box(
            children=[
                self.update_button
            ],
            style=Pack(
                direction=COLUMN,
                background_color=rgb(60, 60, 60),
                padding=5
            )
        )
        self.add(self.update_button_box)
        
        self.display_transaction_list()
        
    def display_transaction_list(self):
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
            self.no_transactions_list_box = toga.Box(
                children=[
                    self.no_transactions_label
                ],
                style=Pack(
                    direction=COLUMN,
                    background_color=rgb(60, 60, 60),
                    padding=(20, 5, 0, 5)
                )
            )
            self.add(self.no_transactions_list_box)
            
            
    def update_transactions_list(self, button):
        self.clear()
        self.add(self.update_button_box)
        self.display_transaction_list()
        
        
    def transaction_window(self, txid):
        self.clear()
        config_path = self.app.paths.config / 'config.json'
        data_info = get_transaction(config_path, txid)
        if data_info:
            total_amount = data_info.get("amount")
            confirmations = data_info.get("confirmations")
            blockhash = data_info.get("blockhash", None)
            blockindex = data_info.get("blockindex")
            expiryheight = data_info.get("expiryheight")
            txid = data_info.get("txid")
            timereceived = data_info.get("timereceived")
            formatted_date_time = datetime.fromtimestamp(timereceived, tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
            details = data_info.get("details")
            for data in details:
                amount = data["amount"]
                address = data.get("address", "Shielded")
                category = data["category"]
                vout = data["vout"]
                size = data["size"]
                
                if category == "send":
                    text = "SEND"
                    text_style = Pack(
                        color=rgb(255, 0, 0),
                        font_size="8",
                        font_family="monospace",
                        font_weight="bold",
                        padding_left=10
                    )
                else:
                    text = "RECEIVE"
                    text_style = Pack(
                        color=rgb(9, 236, 16),
                        font_size="8",
                        font_family="monospace",
                        font_weight="bold",
                        padding_left=10
                    )
                
                self.details_box = toga.Box(
                    children=[
                        toga.Label(
                            "Amount :",
                            style=Pack(
                                color=rgb(240, 248, 255),
                                font_family="monospace",
                                font_size="10",
                                padding=5
                            )
                        ),
                        toga.Label(
                            f"{amount} BTCZ",
                            style=Pack(
                                color=rgb(240, 248, 255),
                                font_family="monospace",
                                font_size="10",
                                padding_left=10
                            )
                        ),
                        toga.Label(
                            "Address :",
                            style=Pack(
                                color=rgb(240, 248, 255),
                                font_family="monospace",
                                font_size="10",
                                padding=5
                            )
                        ),
                        toga.Label(
                            f"{address}",
                            style=Pack(
                                color=rgb(240, 248, 255),
                                font_family="monospace",
                                font_size="10",
                                padding_left=10
                            )
                        ),
                        toga.Label(
                            "Category :",
                            style=Pack(
                                color=rgb(240, 248, 255),
                                font_family="monospace",
                                font_size="10",
                                padding=5
                            )
                        ),
                        toga.Label(
                            f"{text}",
                            style=text_style
                        ),
                        toga.Label(
                            "Vout :",
                            style=Pack(
                                color=rgb(240, 248, 255),
                                font_family="monospace",
                                font_size="10",
                                padding=5
                            )
                        ),
                        toga.Label(
                            f"{vout}",
                            style=Pack(
                                color=rgb(240, 248, 255),
                                font_family="monospace",
                                font_size="10",
                                padding_left=10
                            )
                        ),
                        toga.Label(
                            "Size :",
                            style=Pack(
                                color=rgb(240, 248, 255),
                                font_family="monospace",
                                font_size="10",
                                padding=5
                            )
                        ),
                        toga.Label(
                            f"{size}",
                            style=Pack(
                                color=rgb(240, 248, 255),
                                font_family="monospace",
                                font_size="10",
                                padding_left=10
                            )
                        ),
                    ],
                    style=Pack(
                        direction=COLUMN,
                        background_color=rgb(90, 90, 90),
                        padding=5
                    )
                )
            
            self.more_info_label = toga.Label(
                "Transaction Info",
                style=Pack(
                    color=rgb(240, 248, 255),
                    font_size="12",
                    font_family="monospace",
                    text_align="center"
                )
            )
            
            self.info_divider = toga.Divider(
                direction="HORIZONTAL"
            )
            
            self.total_amount_label = toga.Label(
                "Total Amount :",
                style=Pack(
                    color=rgb(240, 248, 255),
                    font_size="10",
                    font_family="monospace",
                    padding=5
                )
            )
            
            self.total_amount_value = toga.Label(
                f"{total_amount} BTCZ",
                style=Pack(
                    color=rgb(240, 248, 255),
                    font_size="10",
                    font_family="monospace",
                    padding=5
                )
            )
            
            self.confirmations_label = toga.Label(
                "Confirmations :",
                style=Pack(
                    color=rgb(240, 248, 255),
                    font_size="10",
                    font_family="monospace",
                    padding=5
                )
            )
            
            self.confirmations_value = toga.Label(
                f"{confirmations}",
                style=Pack(
                    color=rgb(240, 248, 255),
                    font_size="10",
                    font_family="monospace",
                    padding=5
                )
            )
            
            self.blockhash_label = toga.Label(
                "Blockhash :",
                style=Pack(
                    color=rgb(240, 248, 255),
                    font_size="10",
                    font_family="monospace",
                    padding=5
                )
            )
            
            self.blockhash_value = toga.MultilineTextInput(
                value=f"{blockhash}",
                readonly=True,
                style=Pack(
                    color=rgb(240, 248, 255),
                    font_size="9",
                    font_family="monospace",
                    padding=5
                )
            )
            
            self.blockindex_label = toga.Label(
                "Blockindex :",
                style=Pack(
                    color=rgb(240, 248, 255),
                    font_size="10",
                    font_family="monospace",
                    padding=5
                )
            )
            
            self.blockindex_value = toga.Label(
                f"{blockindex}",
                style=Pack(
                    color=rgb(240, 248, 255),
                    font_size="10",
                    font_family="monospace",
                    padding=5
                )
            )
            
            self.expiryheight_label = toga.Label(
                "Expiryheight :",
                style=Pack(
                    color=rgb(240, 248, 255),
                    font_size="10",
                    font_family="monospace",
                    padding=5
                )
            )
            
            self.expiryheight_value = toga.Label(
                f"{expiryheight}",
                style=Pack(
                    color=rgb(240, 248, 255),
                    font_size="10",
                    font_family="monospace",
                    padding=5
                )
            )
            
            self.timerecieved_label = toga.Label(
                "Date :",
                style=Pack(
                    color=rgb(240, 248, 255),
                    font_size="10",
                    font_family="monospace",
                    padding=5
                )
            )
            
            self.timerecieved_value = toga.Label(
                f"{formatted_date_time}",
                style=Pack(
                    color=rgb(240, 248, 255),
                    font_size="10",
                    font_family="monospace",
                    padding=5
                )
            )
            
            self.more_info_button = toga.Button(
                "close",
                on_press=self.back_transactions_list
            )
            
            self.more_info_box = toga.Box(
                children=[
                    self.more_info_label,
                    self.info_divider,
                    self.total_amount_label,
                    self.total_amount_value,
                    self.confirmations_label,
                    self.confirmations_value,
                    self.blockhash_label,
                    self.blockhash_value,
                    self.blockindex_label,
                    self.blockindex_value,
                    self.expiryheight_label,
                    self.expiryheight_value,
                    self.timerecieved_label,
                    self.timerecieved_value,
                    self.details_box
                ],
                style=Pack(
                    direction=COLUMN,
                    background_color=rgb(70, 70, 70),
                    padding=5
                )
            )
            
            self.more_info_main_box = toga.Box(
                children=[
                    self.more_info_box,
                    self.more_info_button
                ],
                style=Pack(
                    direction=COLUMN,
                    background_color=rgb(60, 60, 60),
                    padding=5
                )
            )
            
            self.add(self.more_info_main_box)
            
    def back_transactions_list(self, button):
        self.clear()
        self.add(self.update_button_box)
        self.display_transaction_list()
