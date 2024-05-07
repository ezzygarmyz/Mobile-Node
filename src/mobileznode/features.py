import toga
from toga.colors import rgb
from toga.style.pack import Pack, COLUMN, ROW

class FeaturesBox(toga.Box):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = None
        
    def set_app(self, app):
        self.app = app
        
        self.display_features_list()
    
    def display_features_list(self):
        self.explorer_button = toga.Button(
            "explorer",
            enabled=True,
            style=Pack(
                background_color=rgb(80, 80, 80),
                color=rgb(240, 248, 255),
                width=125,
                height=100,
                alignment="left",
                font_family="monospace",
                padding=(15, 0 , 15, 15)
            ),
            on_press=self.on_press_explorer
        )
        
        self.blocks_button = toga.Button(
            "blocks",
            enabled=True,
            style=Pack(
                background_color=rgb(80, 80, 80),
                color=rgb(240, 248, 255),
                width=125,
                height=100,
                alignment="right",
                font_family="monospace",
                padding= (15, 15, 15, 0)
            )
        )
        
        self.first_line_space = toga.Box(
            style=Pack(
                background_color=rgb(60, 60, 60),
                flex=1
            )
        )
        
        self.first_line_buttons = toga.Box(
            children=[
                self.explorer_button,
                self.first_line_space,
                self.blocks_button
            ],
            style=Pack(
                direction=ROW,
                padding=5,
                background_color=rgb(60, 60, 60)
            )
        )
        
        self.add(self.first_line_buttons)
        
    
    def display_insight_explorer(self):
        
        self.close_explorer_button = toga.Button(
            "close",
            enabled=True,
            on_press=self.back_features_list
        )
        
        self.explorer_main_box = toga.Box(
            children=[
              self.close_explorer_button  
            ],
            style=Pack(
                direction=COLUMN,
                padding=5,
                background_color=rgb(60, 60, 60)
            )
        )
        
        self.add(self.explorer_main_box)
        
        
    def on_press_explorer(self, button):
        self.clear()
        self.display_insight_explorer()
        
    def back_features_list(self, button):
        self.clear()
        self.display_features_list()
        
