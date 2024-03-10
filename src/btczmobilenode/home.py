import toga
from toga.colors import rgb
from toga.style.pack import Pack, COLUMN, ROW
import asyncio

from .blockchaininfo import get_total_balance, get_blockchain_info, get_unconfirmedbalance

class MainBalanceBox(toga.Box):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = None
    
    def set_app(self, app):
        self.app = app
        config_path = self.app.paths.config / 'config.json'

        total, transparent, private = get_total_balance(config_path)
        
        self.totalbalance_value = toga.Label(
            f"{total} BTCZ",
            style=Pack(
                text_align="center",
                font_size="22",
                font_family="monospace",
                color=rgb(240, 248, 255),
                padding=(10, 0, 0, 0),
                font_weight="bold"
            )
        )
        
        self.unconfirmed_balance = toga.Label(
            f"",
            style=Pack(
                text_align="center",
                font_size="10",
                font_family="monospace",
                font_weight="bold",
                color=rgb(255, 0, 0),
                padding=(5, 0, 0, 0),
            )
        )
        
        self.t_balance_value = toga.Label(
            f"T : {transparent} BTCZ",
            style=Pack(
                text_align="center",
                font_size="10",
                font_family="monospace",
                font_weight="bold",
                color=rgb(235, 186, 6),
                padding=(15, 0, 0, 0)
            )
        )
        
        self.z_balance_value = toga.Label(
            f"Z : {private} BTCZ",
            style=Pack(
                text_align="center",
                font_size="10",
                font_family="monospace",
                font_weight="bold",
                color=rgb(0, 179, 241),
                padding=(2, 0, 50, 0)
            )
        )
        
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
                
                self.totalbalance_value,
                self.unconfirmed_balance,
                self.t_balance_value,
                self.z_balance_value,
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
        
        chain, blocks, header, bestblock, verificationprogress, difficulty, disk_size, commitments = get_blockchain_info(config_path)
        
        self.chain_label = toga.Label(
            f"Chain :",
            style=Pack(
                font_size="10",
                font_family="monospace",
                font_weight="bold",
                text_align="center",
                color=rgb(240, 248, 255),
                padding=5
            )
        )
        
        self.chain_label_box = toga.Box(
            children=[
                self.chain_label
            ],
            style=Pack(
                padding=5,
                flex=1
            )
        )
        
        self.chain_value = toga.Label(
            f"{chain}",
            style=Pack(
                font_size="10",
                font_family="monospace",
                font_weight="bold",
                text_align="center",
                color=rgb(240, 248, 255),
                padding=5
            )
        )
        
        self.chain_value_box = toga.Box(
            children=[
                self.chain_value
            ],
            style=Pack(
                padding=5
            )
        )
        
        self.chain_line = toga.Box(
            children=[
                self.chain_label_box,
                self.chain_value_box
            ],
            style=Pack(
                padding=(5, 20, 5, 20),
                direction=ROW,
                background_color=rgb(70, 70, 70)
            )
        )
        
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
        
        self.bestblock_label = toga.Label(
            f"Bestblock :", 
            style=Pack(
                font_size="10",
                font_family="monospace",
                font_weight="bold",
                text_align="center",
                color=rgb(240, 248, 255),
                padding=5
            )
        )
        
        self.bestblock_label_box = toga.Box(
            children=[
                self.bestblock_label
            ],
            style=Pack(
                padding=5,
                flex=1
            )
        )
        
        self.bestblock_value = toga.Label(
            f"{bestblock}", 
            style=Pack(
                font_size="10",
                font_family="monospace",
                font_weight="bold",
                text_align="center",
                color=rgb(240, 248, 255),
                padding=5
            )
        )
        
        self.bestblock_value_box = toga.Box(
            children=[
                self.bestblock_value
            ],
            style=Pack(
                padding=5
            )
        )
        
        self.bestblock_line = toga.Box(
            children=[
                self.bestblock_label_box,
                self.bestblock_value_box
            ],
            style=Pack(
                padding=(5, 20, 5, 20),
                direction=ROW,
                background_color=rgb(70, 70, 70)
            )
        )
        
        self.verificationprogress_label = toga.Label(
            f"Synchronization :", 
            style=Pack(
                font_size="10",
                font_family="monospace",
                font_weight="bold",
                text_align="center",
                color=rgb(240, 248, 255),
                padding=5
            )
        )
        
        self.verificationprogress_label_box = toga.Box(
            children=[
                self.verificationprogress_label
            ],
            style=Pack(
                padding=5,
                flex=1
            )
        )
        self.verificationprogress_value = toga.Label(
            f"{float(verificationprogress):.2f}%", 
            style=Pack(
                font_size="10",
                font_family="monospace",
                font_weight="bold",
                text_align="center",
                color=rgb(240, 248, 255),
                padding=5
            )
        )
        
        self.verificationprogress_value_box = toga.Box(
            children=[
                self.verificationprogress_value
            ],
            style=Pack(
                padding=5
            )
        )
        
        self.verificationprogress_line = toga.Box(
            children=[
                self.verificationprogress_label_box,
                self.verificationprogress_value_box
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
                self.chain_line,
                self.blocks_line,
                self.headers_line,
                self.bestblock_line,
                self.verificationprogress_line,
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
        
        self.app.add_background_task(
            self.task_update_blockchaininfo
        )
        
        self.app.add_background_task(
            self.task_update_totalbalance
        )
        
        self.app.add_background_task(
            self.task_update_getunconfirmedbalance
        )
        
    async def task_update_blockchaininfo(self, *args):
        config_path = self.app.paths.config / 'config.json'
        while True:
            chain, blocks, header, bestblock, verificationprogress, difficulty, disk_size, commitments = get_blockchain_info(config_path)
            self.chain_value.text = f"{chain}"
            self.blocks_value.text = f"{blocks}"
            self.headers_value.text = f"{header}"
            self.bestblock_value.text = f"{bestblock}"
            self.verificationprogress_value.text = f"{float(verificationprogress):.2f}%"
            self.difficulty_value.text = f"{float(difficulty):.2f}"
            self.sizeondisk_value.text = f"{float(disk_size):.1f} GB"
            self.commitments_value.text = f"{commitments}"
            await asyncio.sleep(15)
            
            
    async def task_update_totalbalance(self, *args):
        config_path = self.app.paths.config / 'config.json'
        while True:
            total, transparent, private = get_total_balance(config_path)
            self.totalbalance_value.text = f"{total} BTCZ"
            self.t_balance_value.text = f"T : {transparent} BTCZ"
            self.z_balance_value.text = f"Z : {private} BTCZ"
            await asyncio.sleep(15)
            
    
    async def task_update_getunconfirmedbalance(self, *args):
        config_path = self.app.paths.config / 'config.json'
        while True:
            unconfirmedbalance = get_unconfirmedbalance(config_path)
            if float(unconfirmedbalance) > 0:
                self.unconfirmed_balance.text = f"UnConf. Bal : {float(unconfirmedbalance)} BTCZ"
            else:
                self.unconfirmed_balance.text = ""
            await asyncio.sleep(15)
