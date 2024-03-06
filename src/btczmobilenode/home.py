import toga
from toga.colors import rgb
from toga.style.pack import Pack, COLUMN, ROW

from btczmobilenode.blockchaininfo import get_total_balance, get_blockchain_info

class MainBalanceBox(toga.Box):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = None
    
    def set_app(self, app):
        self.app = app
        config_path = self.app.paths.config / 'config.json'

        total, transparent, private = get_total_balance(config_path)
        
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
                    style=Pack(
                        text_align="center",
                        font_size="10",
                        font_family="monospace",
                        font_weight="bold",
                        color=rgb(240, 248, 255),
                        padding=(15, 0, 0, 0))),
                
                toga.Label(
                    f"Z : {private} BTCZ",
                    style=Pack(
                        text_align="center",
                        font_size="10",
                        font_family="monospace",
                        font_weight="bold",
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
                        font_size="11",
                        font_weight="bold",
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
        
        blocks, header, difficulty, disk_size, commitments = get_blockchain_info(config_path)
        
        self.blocks_label = toga.Label(
            f"Blocks :",
            style=Pack(
                font_size="10",
                font_family="monospace",
                font_weight="bold",
                text_align="center",
                color=rgb(240, 248, 255),
                padding=5
            )
        )
        
        self.blocks_label_box = toga.Box(
            children=[
                self.blocks_label
            ],
            style=Pack(
                padding=5,
                flex=1
            )
        )
        
        self.blocks_value = toga.Label(
            f"{blocks}",
            style=Pack(
                font_size="10",
                font_family="monospace",
                font_weight="bold",
                text_align="center",
                color=rgb(240, 248, 255),
                padding=5
            )
        )
        
        self.blocks_value_box = toga.Box(
            children=[
                self.blocks_value
            ],
            style=Pack(
                padding=5
            )
        )
        
        self.blocks_line = toga.Box(
            children=[
                self.blocks_label_box,
                self.blocks_value_box
            ],
            style=Pack(
                padding=(5, 20, 5, 20),
                direction=ROW,
                background_color=rgb(70, 70, 70)
            )
        )
        
        self.headers_label = toga.Label(
            f"Headers :", 
            style=Pack(
                font_size="10",
                font_family="monospace",
                font_weight="bold",
                text_align="center",
                color=rgb(240, 248, 255),
                padding=5
            )
        )
        
        self.headers_label_box = toga.Box(
            children=[
                self.headers_label
            ],
            style=Pack(
                padding=5,
                flex=1
            )
        )
        
        self.headers_value = toga.Label(
            f"{header}", 
            style=Pack(
                font_size="10",
                font_family="monospace",
                font_weight="bold",
                text_align="center",
                color=rgb(240, 248, 255),
                padding=5
            )
        )
        
        self.headers_value_box = toga.Box(
            children=[
                self.headers_value
            ],
            style=Pack(
                padding=5
            )
        )
        
        self.headers_line = toga.Box(
            children=[
                self.headers_label_box,
                self.headers_value_box
            ],
            style=Pack(
                padding=(5, 20, 5, 20),
                direction=ROW,
                background_color=rgb(70, 70, 70)
            )
        )
        
        self.difficulty_label = toga.Label(
            f"Difficulty :",
            style=Pack(
                font_size="10",
                font_family="monospace",
                font_weight="bold",
                text_align="center",
                color=rgb(240, 248, 255),
                padding=5
            )
        )
        
        self.difficulty_label_box = toga.Box(
            children=[
                self.difficulty_label
            ],
            style=Pack(
                padding=5,
                flex=1
            )
        )
        
        self.difficulty_value = toga.Label(
            f"{float(difficulty):.2f}",
            style=Pack(
                font_size="10",
                font_family="monospace",
                font_weight="bold",
                text_align="center",
                color=rgb(240, 248, 255),
                padding=5
            )
        )
        
        self.difficulty_value_box = toga.Box(
            children=[
                self.difficulty_value
            ],
            style=Pack(
                padding=5
            )
        )
        
        self.difficulty_line = toga.Box(
            children=[
                self.difficulty_label_box,
                self.difficulty_value_box
            ],
            style=Pack(
                padding=(5, 20, 5, 20),
                direction=ROW,
                background_color=rgb(70, 70, 70)
            )
        )
        
        self.commitments_label = toga.Label(
            f"Commitments :",
            style=Pack(
                font_size="10",
                font_family="monospace",
                font_weight="bold",
                text_align="center",
                color=rgb(240, 248, 255),
                padding=5
            )
        )
        
        self.commitments_label_box = toga.Box(
            children=[
                self.commitments_label
            ],
            style=Pack(
                padding=5,
                flex=1
            )
        )
        
        self.commitments_value = toga.Label(
            f"{commitments}",
            style=Pack(
                font_size="10",
                font_family="monospace",
                font_weight="bold",
                text_align="center",
                color=rgb(240, 248, 255),
                padding=5
            )
        )
        
        self.commitments_value_box = toga.Box(
            children=[
                self.commitments_value
            ],
            style=Pack(
                padding=5
            )
        )
        
        self.commitments_line = toga.Box(
            children=[
                self.commitments_label_box,
                self.commitments_value_box
            ],
            style=Pack(
                padding=(5, 20, 5, 20),
                direction=ROW,
                background_color=rgb(70, 70, 70)
            )
        )
        
        self.sizeondisk_label = toga.Label(
            f"Size On Disk :",
            style=Pack(
                font_size="10",
                font_family="monospace",
                font_weight="bold",
                text_align="center",
                color=rgb(240, 248, 255),
                padding=5
            )
        )
        
        self.sizeondisk_label_box = toga.Box(
            children=[
                self.sizeondisk_label
            ],
            style=Pack(
                padding=5,
                flex=1
            )
        )
        
        self.sizeondisk_value = toga.Label(
            f"{float(disk_size):.1f} GB",
            style=Pack(
                font_size="10",
                font_family="monospace",
                font_weight="bold",
                text_align="center",
                color=rgb(240, 248, 255),
                padding=5
            )
        )
        
        self.sizeondisk_value_box = toga.Box(
            children=[
                self.sizeondisk_value
            ],
            style=Pack(
                padding=5
            )
        )
        
        self.sizeondisk_line = toga.Box(
            children=[
                self.sizeondisk_label_box,
                self.sizeondisk_value_box
            ],
            style=Pack(
                padding=(5, 20, 5, 20),
                direction=ROW,
                background_color=rgb(70, 70, 70)
            )
        )
        
        self.blockchain_info = toga.Box(
            children=[
                self.blocks_line,
                self.headers_line,
                self.difficulty_line,
                self.commitments_line,
                self.sizeondisk_line
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
