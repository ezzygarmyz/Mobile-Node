import toga
from toga.colors import rgb
from toga.style.pack import Pack, COLUMN
import requests
import json
import os


class WalletBox(toga.Box):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.receive_box = toga.Box(
            children=[
                toga.Label(
                    f"Select Address :",
                    style=Pack(font_size="10",
                            font_family="monospace",
                            color=rgb(240, 248, 255),
                            padding=(10, 0, 0, 10)
                        )
                )
            ],
            style=Pack(direction=COLUMN,
                       background_color=rgb(60, 60, 60),
                       padding=5)
        )
        
        self.add(self.receive_box)