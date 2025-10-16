

from bibliotecas import *


class TelaPedido(Screen):
    def __init__(self, **kwargs):
        self.app = MDApp.get_running_app()
        super().__init__(**kwargs)