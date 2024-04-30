import os
import json
import toga
from toga.colors import rgb
from toga.style.pack import COLUMN, Pack


class RPCSettingsBox(toga.Box):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = None
        self.setting_command = None

    def set_app(self, app, setting_command):
        self.app = app
        self.setting_command = setting_command
        
        self.config_note = toga.Box(
            children=[
                toga.Label(
                    "Note : please enter the same config"
                    "\nthat where set in your bitcoinz.conf file.",
                    style=Pack(
                        padding=5,
                        font_family="monospace",
                        color=rgb(235, 186, 6),
                        font_size="9",
                        flex=1)
                )
            ],
            style=Pack(
                direction=COLUMN,
                background_color=rgb(60, 60, 60),
                padding=5)
        )
        
        self.rpc_user_box = toga.Box(
            children=[
                toga.Label(
                    "rpcuser :",
                    style=Pack(
                        font_size="10",
                        font_family="monospace",
                        color=rgb(240, 248, 255),
                        padding=(10, 0, 0, 10)
                    )
                ),
                
                toga.TextInput(
                    placeholder="",
                    style=Pack(
                        font_size="10",
                        font_family="monospace",
                        color=rgb(0, 179, 241),
                        padding=(5, 0, 10, 10)
                    )
                )
            ],
            style=Pack(
                direction=COLUMN,
                background_color=rgb(60, 60, 60),
                padding=5)
        )
        
        self.rpc_password_box = toga.Box(
            children=[
                toga.Label(
                    f"rpcpassword",
                    style=Pack(
                        font_size="10",
                        font_family="monospace",
                        color=rgb(240, 248, 255),
                        padding=(10, 0, 0, 10)
                    )
                ),
                
                toga.PasswordInput(
                    placeholder="",
                    style=Pack(
                        font_size="10",
                        font_family="monospace",
                        color=rgb(0, 179, 241),
                        padding=(5, 0, 10, 10)
                    )
                )
            ],
            style=Pack(
                direction=COLUMN,
                background_color=rgb(60, 60, 60),
                padding=5)
        )
        
        self.rpc_host_box = toga.Box(
            children=[
                toga.Label(
                    "rpchost :",
                    style=Pack(
                        font_size="10",
                        font_family="monospace",
                        color=rgb(240, 248, 255),
                        padding=(10, 0, 0, 10)
                    )
                ),
                
                toga.TextInput(
                    placeholder="",
                    style=Pack(
                        font_size="10",
                        font_family="monospace",
                        color=rgb(0, 179, 241),
                        padding=(5, 0, 10, 10)
                    )
                ),
                toga.Label(
                    f"for local connection set [ localhost ]",
                    style=Pack(
                        font_size="8",
                        font_family="monospace",
                        color=rgb(235, 186, 6),
                        padding=(0, 0, 5, 10)
                    )
                )
            ],
            style=Pack(
                direction=COLUMN,
                background_color=rgb(60, 60, 60),
                padding=5)
        )
        
        self.rpc_port_box = toga.Box(
            children=[
                toga.Label(
                    "rpcport :",
                    style=Pack(
                        font_size="10",
                        font_family="monospace",
                        color=rgb(240, 248, 255),
                        padding=(10, 0, 0, 10)
                    )
                ),
                
                toga.NumberInput(
                    style=Pack(
                        font_size="10",
                        font_family="monospace",
                        color=rgb(0, 179, 241),
                        padding=(5, 0, 10, 10)
                    )
                )
            ],
            style=Pack(
                direction=COLUMN,
                background_color=rgb(60, 60, 60),
                padding=5)
        )
        
        self.save_button = toga.Button(
            "Save",
            enabled=True,
            style=Pack(
                flex=1,
                font_family="monospace",
                padding=5,
                font_weight="bold",),
            on_press=self.save_settings)
                
        self.cancel_button = toga.Button(
            "EXIT",
            enabled=True,
            style=Pack(
                flex=1,
                font_family="monospace",
                padding=5,
                font_weight="bold"),
            on_press=self.back_to_main)
        
        self.space_box = toga.Box(
            style=Pack(
                direction=COLUMN,
                background_color=rgb(25, 25, 25),
                flex=1
            )
        )
        
        self.settings_buttons = toga.Box(
            children=[
                self.save_button, self.cancel_button
            ],
            style=Pack(
                alignment="bottom",
                background_color=rgb(60, 60, 60),
                padding=5)
        )
        
        self.add(self.config_note,
                 self.rpc_user_box,
                 self.rpc_password_box,
                 self.rpc_host_box,
                 self.rpc_port_box,
                 self.space_box,
                 self.settings_buttons)
    
    def save_settings(self, button):
        # Get values from input widgets
        rpcuser = self.rpc_user_box.children[1].value
        rpcpassword = self.rpc_password_box.children[1].value
        rpchost = self.rpc_host_box.children[1].value
        rpcport = int(self.rpc_port_box.children[1].value)

        # Create a dictionary with the new configuration settings
        new_config = {
            'rpcuser': rpcuser,
            'rpcpassword': rpcpassword,
            'rpchost': rpchost,
            'rpcport': rpcport
        }

        config_path = self.app.paths.config / 'config.json'
        
        # Check if the config file exists
        if not os.path.exists(config_path):
            # Create the directory if it doesn't exist
            os.makedirs(config_path.parent, exist_ok=True)

        if os.path.exists(config_path):
            # Load existing configuration from the file
            with open(config_path, 'r') as f:
                existing_config = json.load(f)
        else:
            existing_config = {}
            
        # Compare new config with existing config
        if new_config == existing_config:
            # No changes, revert back to the original settings
            self.setting_command.enabled = True
            self.app.main_window.content = self.app.option_container
            return

        existing_config.update(new_config)

        config_json = json.dumps(existing_config, indent=4)

        # Write the JSON data to the file
        with open(config_path, 'w') as f:
            f.write(config_json)
        self.app.main_window.info_dialog("Done !", "RPC config have been saved")
        self.setting_command.enabled = True
        self.app.main_window.content = self.app.option_container

    def back_to_main(self, button):
        self.setting_command.enabled = True
        self.app.main_window.content = self.app.option_container