import toga
from toga.colors import rgb
from toga.style.pack import Pack, COLUMN
import asyncio

from .listaddresses import get_t_addresses, get_z_addresses
from .getbalance import get_address_balance
from .validaddress import t_validate, z_validate
from .operations import new_operation_t, new_operation_z, new_operation_z_memo, check_operation_status


class SendBox(toga.Box):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = None
        self.config_path = None
    
    def set_app(self, app):
        self.app = app
        self.config_path = self.app.paths.config / 'config.json'
        
        accoun_t_data = get_t_addresses(self.config_path)
        if accoun_t_data:
            sorted_addresses = sorted(
                [address_info for address_info_list in accoun_t_data for address_info in address_info_list],
                key=lambda x: x[1],
                reverse=True
            )
            if len(sorted_addresses) == 1:
                self.address_t_items = [(None, ""), (sorted_addresses[0][0], sorted_addresses[0][0])]
            else:
                self.address_t_items = [(None, "")] + [(address_info[0], address_info[0]) for address_info in sorted_addresses]
        else:
            self.address_t_items = [(None, "")]
            
            
        accoun_z_data = get_z_addresses(self.config_path)
        if accoun_z_data:
            if len(accoun_z_data) == 1:
                self.address_z_items = [(None, ""), (accoun_z_data[0], accoun_z_data[0])]
            else:
                self.address_z_items = [(None, "")] + [(address, address) for address in accoun_z_data]
        else:
            self.address_z_items = [(None, "")]
            
        self.switch_label = toga.Label(
                    f"Switch",
                    style=Pack(
                        font_size="12",
                        font_family="monospace",
                        text_align="center",
                        color=rgb(240, 248, 255),
                        padding=5,
                        font_weight="bold"
                    )
        )
        
        self.switch = toga.Switch(
                    "Transparent",
                    enabled=True,
                    value=False,
                    style=Pack(
                        font_size="12",
                        font_family="monospace",
                        color=rgb(235, 186, 6),
                        padding=(5, 20, 5, 20),
                        font_weight="bold"
                    ),
                    on_change=self.on_change_switch
        )
        
        self.send_switcher_box = toga.Box(
            children=[
                self.switch_label, self.switch
            ],
            style=Pack(
                direction=COLUMN,
                background_color=rgb(60, 60, 60),
                padding=(5, 5, 20, 5)
            )
        )
        
        self.selection_t = toga.Selection(
            accessor="address",
            items=self.address_t_items, 
            enabled=True,
            on_change=self.on_change_t_selection,
            style=Pack(
                padding=(5, 0, 10, 10),
                color=rgb(235, 186, 6)
            )
        )
        
        self.selection_t_box = toga.Box(
            children=[
                self.selection_t
            ],
            style=Pack(
                direction=COLUMN,
                background_color=rgb(90, 90, 90),
                padding=5,
            )
        )
        
        self.t_address_box = toga.Box(
            children=[
                toga.Label(
                    f"From Address :",
                    style=Pack(
                        font_size="10",
                        font_family="monospace",
                        color=rgb(235, 186, 6),
                        padding=(10, 0, 0, 10)
                    )
                ),
                self.selection_t_box
            ],
            style=Pack(
                direction=COLUMN,
                background_color=rgb(60, 60, 60),
                padding=5
            )
        )
        
        self.address_input = toga.TextInput(
            placeholder="Paste address here",
            on_change=self.validate_address,
            style=Pack(
                font_size="12",
                font_family="monospace",
                color=rgb(240, 248, 255),
                padding=(5, 0, 10, 10)
            )
        )
        
        self.t_label_validate = toga.Label(
            "",
            style=Pack(
                font_family="monospace",
                text_align="center",
            )
        )
        
        self.addressinput_t_box = toga.Box(
            children=[
                self.t_label_validate,
                self.address_input
            ],
            style=Pack(
                direction=COLUMN,
                background_color=rgb(90, 90, 90),
                padding=5,
            )
        )
        
        self.send_to_label = toga.Label(
            f"Send to :",
            style=Pack(
                font_size="10",
                font_family="monospace",
                color=rgb(235, 186, 6),
                padding=(10, 0, 0, 10)
            )
        )
                
        self.send_t_box = toga.Box(
            children=[
                self.send_to_label,
                self.addressinput_t_box
            ],
            style=Pack(
                direction=COLUMN,
                background_color=rgb(60, 60, 60),
                padding=5)
        )
        
        self.amount_t = toga.NumberInput(
            step=0.00000001,
            min=0.00000001,
            style=Pack(
                font_family="monospace",
                color=rgb(240, 248, 255),
                padding=(5, 0, 10, 10),
            ),
            on_change=self.check_balance_t
        )
        
        self.check_amount_t_label = toga.Label(
            "",
            style=Pack(
                font_family="monospace",
                font_size="10",
                text_align="center"
            )
        )
            
        self.amount_t_box = toga.Box(
            children=[
                toga.Label(
                    f"Amount :",
                    style=Pack(
                        font_size="10",
                        font_family="monospace",
                        color=rgb(235, 186, 6),
                        padding=(10, 0, 0, 10)
                    )
                ),
                self.check_amount_t_label,
                self.amount_t
            ],
            style=Pack(
                direction=COLUMN,
                background_color=rgb(60, 60, 60),
                padding=5)
        )
        
        self.fee_input = toga.NumberInput(
            value=0.0001,
            step=0.00000001,
            min=0.00000001,
            style=Pack(
                font_family="monospace",
                color=rgb(240, 248, 255),
                padding=(5, 0, 10, 10),
            ),
        )
        
        self.fee_label = toga.Label(
            f"Fee : [optional]",
            style=Pack(
                font_size="10",
                font_family="monospace",
                color=rgb(235, 186, 6),
                padding=(10, 0, 0, 10)
            )
        )
        
        self.transaction_fee_box = toga.Box(
            children=[
                self.fee_label,
                self.fee_input
            ],
            style=Pack(
                direction=COLUMN,
                background_color=rgb(60, 60, 60),
                padding=5
            )
        )
        
        self.space_box = toga.Box(
            style=Pack(
                direction=COLUMN,
                flex=1,
                background_color=rgb(25, 25, 25)
            )
        )  
        
        self.button_t_send = toga.Button(
            "SEND",
            enabled=True,
            style=Pack(
                padding=5,
                background_color=rgb(235, 186, 6),
                color=rgb(240, 248, 255),
                font_family="monospace",
            ),
            on_press=self.on_press_button_t
        )
        
        self.button_t_box = toga.Box(
            children=[
                self.button_t_send
            ],
            style=Pack(
                direction=COLUMN,
                background_color=rgb(60, 60, 60),
                padding=5
            )
        )  
        
        self.add(
            self.send_switcher_box,
            self.t_address_box,
            self.send_t_box,
            self.amount_t_box,
            self.transaction_fee_box,
            self.space_box,
            self.button_t_box)
        
        self.selection_z = toga.Selection(
            accessor="address",
            items=self.address_z_items, 
            enabled=True,
            on_change=self.on_change_z_selection,
            style=Pack(
                padding=(5, 0, 10, 10),
                color=rgb(235, 186, 6)
            )
        )
        
        self.selection_z_box = toga.Box(
            children=[
                self.selection_z
            ],
            style=Pack(
                direction=COLUMN,
                background_color=rgb(90, 90, 90),
                padding=5,
            )
        )
        
        self.z_address_box = toga.Box(
            children=[
                toga.Label(
                    f"From Address :",
                    style=Pack(
                        font_size="10",
                        font_family="monospace",
                        color=rgb(0, 179, 241),
                        padding=(10, 0, 0, 10)
                    )
                ),
                self.selection_z_box
            ],
            style=Pack(
                direction=COLUMN,
                background_color=rgb(60, 60, 60),
                padding=5)
        )
        
        self.amount_z = toga.NumberInput(
            step=0.00000001,
            min=0.00000001,
            style=Pack(
                font_family="monospace",
                color=rgb(240, 248, 255),
                padding=(5, 0, 10, 10),
            ),
            on_change=self.check_balance_z
        )
        
        self.check_amount_z_label = toga.Label(
            "",
            style=Pack(
                font_family="monospace",
                font_size="10",
                text_align="center"
            )
        )
            
        self.amount_z_box = toga.Box(
            children=[
                toga.Label(
                    f"Amount :",
                    style=Pack(
                        font_size="10",
                        font_family="monospace",
                        color=rgb(0, 179, 241),
                        padding=(10, 0, 0, 10)
                    )
                ),
                self.check_amount_z_label,
                self.amount_z
                
            ],
            style=Pack(
                direction=COLUMN,
                background_color=rgb(60, 60, 60),
                padding=5
            )
        )
        
        self.memo_text_input = toga.MultilineTextInput(
            placeholder="[Optional]",
            style=Pack(
                font_family="monospace",
                color=rgb(240, 248, 255),
                padding=(5, 0, 10, 10),
            )
        )
        
        self.memo_input_box = toga.Box(
            children=[
                self.memo_text_input
            ],
            style=Pack(
                direction=COLUMN,
                background_color=rgb(90, 90, 90),
                padding=5,
            )
        )
        
        self.memo_box = toga.Box(
            children=[
                toga.Label(
                    "Memo : [optional]",
                    style=Pack(
                        font_size="10",
                        font_family="monospace",
                        color=rgb(0, 179, 241),
                        padding=(10, 0, 0, 10)
                    )
                ),
                self.memo_input_box
            ],
            style=Pack(
                direction=COLUMN,
                background_color=rgb(60, 60, 60),
                padding=5
                )
        )
        
        self.button_z_send = toga.Button(
            "SEND",
            enabled=True,
            style=Pack(
                padding=5,
                background_color=rgb(0, 179, 241),
                color=rgb(240, 248, 255),
                font_family="monospace",
            ),
            on_press=self.on_press_button_z
        )
        
        self.button_z_box = toga.Box(
            children=[
                self.button_z_send
            ],
            style=Pack(
                direction=COLUMN,
                background_color=rgb(60, 60, 60),
                padding=5
            )
        )
        
        
    async def on_change_switch(self, switch):
        if switch.value:
            self.switch.text = "Shielded"
            self.switch.style.color = rgb(0, 179, 241)
            self.send_to_label.style.color = rgb(0, 179, 241)
            self.fee_label.style.color = rgb(0, 179, 241)
            self.selection_t.items.clear()
            self.selection_z.items = self.address_z_items    
            self.remove(
                self.t_address_box,
                self.send_t_box,
                self.amount_t_box,
                self.transaction_fee_box,
                self.space_box,
                self.button_t_box
            )
            self.add(
                self.z_address_box,
                self.send_t_box,
                self.amount_z_box,
                self.transaction_fee_box,
                self.memo_box,
                self.space_box,
                self.button_z_box
            ) 
        else:
            self.switch.text = "Transparent"
            self.switch.style.color = rgb(235, 186, 6)
            self.send_to_label.style.color = rgb(235, 186, 6)
            self.fee_label.style.color = rgb(235, 186, 6)
            self.selection_z.items.clear()
            self.selection_t.items = self.address_t_items 
            self.remove(
                self.z_address_box,
                self.send_t_box,
                self.amount_z_box,
                self.transaction_fee_box,
                self.memo_box,
                self.space_box,
                self.button_z_box
            )
            self.add(
                self.t_address_box,
                self.send_t_box,
                self.amount_t_box,
                self.transaction_fee_box,
                self.space_box,
                self.button_t_box
            )
            
    
    def on_press_button_t(self, button):
        if self.selection_t.value.address is None:
            self.app.main_window.error_dialog("Error", "Please select an address first.")
        elif self.amount_t.value is None:
            self.app.main_window.error_dialog("Error", "Please enter an amount first.")
        elif self.address_input.value == "":
            self.app.main_window.error_dialog("Error", "Please enter the address you want to send to.")
        else:
            self.address_t = self.selection_t.value.address
            self.toaddress = self.address_input.value
            self.amount_t = self.amount_t.value
            self.tx_fee = self.fee_input.value
            self.app.main_window.confirm_dialog(
                "Details :",
                f"- From : {self.address_t}\n- To : {self.toaddress}\n- Amount : {self.amount_t} BTCZ\n- Fee : {self.tx_fee} BTCZ",
                on_result=self.confirm_t_transaction
            )
            
    def confirm_t_transaction(self, widget, result):
        if result:
            config_path = self.app.paths.config / 'config.json'
            operation_id = new_operation_t(config_path, self.address_t, self.toaddress, self.amount_t, self.tx_fee)
            if operation_id:
                self.selection_t.items.clear()
                self.selection_t.items = self.address_t_items
                self.address_input.value = ""
                operation_status = check_operation_status(config_path, operation_id)
                if isinstance(operation_status, list) and operation_status:
                    status = operation_status[0].get("status")
                    creation_time = operation_status[0].get("creation_time")
                    self.app.main_window.info_dialog("Sent !", f"- Status : {status}\n- Creation time : {creation_time}")
                    
                
        
    def on_press_button_z(self, button):
        if self.selection_z.value.address is None:
            self.app.main_window.error_dialog("Error", "Please select an address first.")
        elif self.amount_z.value is None:
            self.app.main_window.error_dialog("Error", "Please enter an amount first.")
        elif self.address_input.value == "":
            self.app.main_window.error_dialog("Error", "Please enter the address you want to send to.")
            
        else:
            self.address_z = self.selection_z.value.address
            self.toaddress = self.address_input.value
            self.amount_z = self.amount_z.value
            self.tx_fee = self.fee_input.value
            if self.memo_text_input.value == "":
                self.app.main_window.confirm_dialog(
                    "Details :",
                    f"- From : {self.address_z}\n- To : {self.toaddress}\n- Amount : {self.amount_z} BTCZ\n- Fee : {self.tx_fee} BTCZ",
                    on_result=self.confirm_z_transaction
                )
            else:
                self.memo = self.memo_text_input.value
                self.app.main_window.confirm_dialog(
                    "Details :",
                    f"- From : {self.address_z}\n- To : {self.toaddress}\n- Amount : {self.amount_z} BTCZ\n- Fee : {self.tx_fee} BTCZ\n- Memo : {self.memo}",
                    on_result=self.confirm_z_memo_transaction
                )
            
    def confirm_z_transaction(self, widget, result):
        if result:
            config_path = self.app.paths.config / 'config.json'
            operation_id = new_operation_z(config_path, self.address_z, self.toaddress, self.amount_z, self.tx_fee)
            if operation_id:
                self.selection_z.items.clear()
                self.selection_z.items = self.address_z_items
                self.address_input.value = ""
                operation_status = check_operation_status(config_path, operation_id)
                if isinstance(operation_status, list) and operation_status:
                    status = operation_status[0].get("status")
                    creation_time = operation_status[0].get("creation_time")
                    self.app.main_window.info_dialog("Sent !", f"- Status : {status}\n- Creation time : {creation_time}")
                    
                    
    def confirm_z_memo_transaction(self, widget, result):
        if result:
            config_path = self.app.paths.config / 'config.json'
            operation_id = new_operation_z_memo(config_path, self.address_z, self.toaddress, self.amount_z, self.tx_fee, self.memo)
            if operation_id:
                self.selection_z.items.clear()
                self.selection_z.items = self.address_z_items
                self.address_input.value = ""
                operation_status = check_operation_status(config_path, operation_id)
                if isinstance(operation_status, list) and operation_status:
                    status = operation_status[0].get("status")
                    creation_time = operation_status[0].get("creation_time")
                    self.app.main_window.info_dialog("Sent !", f"- Status : {status}\n- Creation time : {creation_time}")
                   
                
    async def on_change_t_selection(self, selection):
        selected_address = selection.value.address if selection.value else None
        if selected_address:
            config_path = self.app.paths.config / 'config.json'
            balance_t = get_address_balance(config_path, selected_address)
            new_balance_t_label = toga.Label(
                f"Available : {balance_t} BTCZ",
                style=Pack(
                    color=rgb(235, 186, 6),
                    font_size="8",
                    text_align="center",
                    font_family="monospace",
                    font_weight="bold",
                    padding=5                  
                )
            )
            if hasattr(self, 'current_t_balance_label'):
                self.t_address_box.remove(self.current_t_balance_label)
            self.current_t_balance_label = new_balance_t_label
            await asyncio.sleep(1)
            self.t_address_box.add(self.current_t_balance_label)
            
            if self.amount_t.value is not None:
                await self.check_balance_t(self.amount_t)
        else:
            if hasattr(self, 'current_t_balance_label'):
                self.t_address_box.remove(self.current_t_balance_label)
                
                
                
    async def on_change_z_selection(self, selection):
        selected_address = selection.value.address if selection.value else None
        if selected_address:
            config_path = self.app.paths.config / 'config.json'
            balance_z = get_address_balance(config_path, selected_address)
            new_balance_z_label = toga.Label(
                f"Available : {balance_z} BTCZ",
                style=Pack(
                    color=rgb(0, 179, 241),
                    font_size="8",
                    text_align="center",
                    font_family="monospace",
                    font_weight="bold",
                    padding=5             
                )
            )
            if hasattr(self, 'current_z_balance_label'):
                self.z_address_box.remove(self.current_z_balance_label)
            self.current_z_balance_label = new_balance_z_label
            await asyncio.sleep(1)
            self.z_address_box.add(self.current_z_balance_label)
            
            if self.amount_z.value is not None:
                await self.check_balance_z(self.amount_z)
        else:
            if hasattr(self, 'current_z_balance_label'):
                self.z_address_box.remove(self.current_z_balance_label)
                
    
    def check_balance_t(self, number_input):
        selected_address = self.selection_t.value.address if self.selection_t.value else None
        entered_amount = number_input.value
        if selected_address and entered_amount is not None:
            config_path = self.app.paths.config / 'config.json'
            balance_t = get_address_balance(config_path, selected_address)
            if entered_amount > balance_t:
                self.check_amount_t_label.text = "Insufficient Balance !"
                self.check_amount_t_label.style.color=rgb(236, 8, 8)
                number_input.value = None
            else:
                self.check_amount_t_label.text = ""
        elif entered_amount is not None:
            self.check_amount_t_label.text = "Select Address"
            self.check_amount_t_label.style.color=rgb(236, 8, 8)
            number_input.value = None
            
            
    def check_balance_z(self, number_input):
        selected_address = self.selection_z.value.address if self.selection_z.value else None
        entered_amount = number_input.value
        if selected_address and entered_amount is not None:
            config_path = self.app.paths.config / 'config.json'
            balance_z = get_address_balance(config_path, selected_address)
            if entered_amount > balance_z:
                self.check_amount_z_label.text = "Insufficient Balance !"
                self.check_amount_z_label.style.color=rgb(236, 8, 8)
                number_input.value = None
            else:
                self.check_amount_z_label.text = ""
        elif entered_amount is not None:
            self.check_amount_z_label.text = "Select Address"
            self.check_amount_z_label.style.color=rgb(236, 8, 8)
            number_input.value = None
                
                
    def validate_address(self, widget):
        
        if self.address_input.value.startswith('t'):
            self.transparent_validate(self.address_input.value)
            
        elif self.address_input.value.startswith('z'):
            self.shielded_validate(self.address_input.value)
            
        else:
            self.t_label_validate.text = "Invalid Address!"
            self.t_label_validate.style.color = rgb(236, 8, 8)
            

    def transparent_validate(self, address):
        config_path = self.app.paths.config / 'config.json'
        is_valid = t_validate(config_path, address)
        if is_valid:
            self.t_label_validate.text = "Valid Address!"
            self.t_label_validate.style.color = rgb(12, 223, 19)
        else:
            self.t_label_validate.text = "Invalid Address!"
            self.t_label_validate.style.color = rgb(236, 8, 8)
            self.address_input.value = None
                        

    def shielded_validate(self, address):
        config_path = self.app.paths.config / 'config.json'
        is_valid = z_validate(config_path, address)   
        if is_valid:
            self.t_label_validate.text = "Valid Address!"
            self.t_label_validate.style.color = rgb(12, 223, 19)
        else:
            self.t_label_validate.text = "Invalid Address!"
            self.t_label_validate.style.color = rgb(236, 8, 8)
            self.address_input.value = None