import toga
from toga.colors import rgb
from toga.style.pack import COLUMN, Pack
import json
import os

from .home import MainBalanceBox
from .send import SendBox
from .wallet import WalletBox
from .settings import RPCSettingsBox
from .transactions import TransactionsBox
from .features import FeaturesBox


class MobileApp(toga.App):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        
    def startup(self):
        
        self.main_balance_box = MainBalanceBox(
            style=Pack(
                direction=COLUMN,
                background_color=rgb(25, 25, 25)
            )
        )
        self.main_balance_box.set_app(self)
        
        self.main_send_box = SendBox(
            style=Pack(
                direction=COLUMN,
                background_color=rgb(25, 25, 25)
            )
        )
        self.main_send_box.set_app(self)
        
        self.main_wallet_box = WalletBox(
            style=Pack(
                direction=COLUMN,
                background_color=rgb(25, 25, 25)
            )
        )
        
        self.main_transactions_box = TransactionsBox(
            style=Pack(
                direction=COLUMN,
                background_color=rgb(25, 25, 25)
            )
        )
        self.main_transactions_box.set_app(self)
        
        
        self.main_features_box = FeaturesBox(
            style=Pack(
                direction=COLUMN,
                background_color=rgb(25, 25, 25)
            )
        )
        self.main_features_box.set_app(self)
        
        self.setting_command = toga.Command(
            action=self.rpc_settings,
            text="Settings",
            tooltip="Setup RPC connection",
            enabled=True
        )
        
        self.rpc_settings_box = RPCSettingsBox(
            style=Pack(
                direction=COLUMN,
                background_color=rgb(25, 25, 25)
            )
        )
        self.rpc_settings_box.set_app(self, self.setting_command)
        
        self.main_balance_scroll = toga.ScrollContainer(
            content=self.main_balance_box,
            vertical=True,
            horizontal=False
        )
        
        self.main_send_scorll = toga.ScrollContainer(
            content=self.main_send_box,
            vertical=True,
            horizontal=False
        )
        
        self.main_transactions_scorll = toga.ScrollContainer(
            content=self.main_transactions_box,
            vertical=True,
            horizontal=False
        )
        
        self.main_features_scorll = toga.ScrollContainer(
            content=self.main_features_box,
            vertical=True,
            horizontal=False
        )

        # Create OptionContainer
        self.option_container = toga.OptionContainer(
            content=[
                toga.OptionItem(
                    "Main",
                    self.main_balance_scroll,
                    enabled=True),
                
                toga.OptionItem(
                    "Txns",
                    self.main_transactions_scorll,
                    enabled=True),
                
                toga.OptionItem(
                    "Send",
                    self.main_send_scorll,
                    enabled=True),
                
                toga.OptionItem(
                    "Wallet",
                    self.main_wallet_box,
                    enabled=True),
                
                toga.OptionItem(
                    "Features",
                    self.main_features_box,
                    enabled=True),
            ],
        )

        # Set up the main window with the OptionContainer
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = self.option_container
        self.main_window.toolbar.add(
            self.setting_command
        )

        # Show the main window
        self.main_window.show()
        
        config_path = self.paths.config / 'config.json'
        if not os.path.exists(config_path):
            self.main_window.info_dialog("No Config !", "Set your RPC config by click on Settings button.")
        
    async def rpc_settings(self, widget):
        config_path = self.paths.config / 'config.json'
        
        # Switch the content of the main window to the RPCSettingsBox
        self.setting_command.enabled = False
        self.main_window.content = self.rpc_settings_box

        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                config = json.load(f)
                self.rpc_settings_box.rpc_user_box.children[1].value = config.get('rpcuser', '')
                self.rpc_settings_box.rpc_password_box.children[1].value = config.get('rpcpassword', '')
                self.rpc_settings_box.rpc_host_box.children[1].value = config.get('rpchost', '')
                self.rpc_settings_box.rpc_port_box.children[1].value = config.get('rpcport', '')
        

def main():
    app = MobileApp(
        icon="resources/logo.png",
        formal_name="Mobile Node",
        app_id="com.btcz.bitcoinz",
        home_page="https://www.getbtcz.com",
        version="1.0.0",
        author="EzzyG",
        
    )
    return app


if __name__ == "__main__":
    app = main()
    app.main_loop()
