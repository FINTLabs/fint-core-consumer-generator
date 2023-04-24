class Model:
    def __init__(self, name: str):
        self.name: str = name
        self.writeable: bool = False
        self.abstract: bool = False
        self.common: bool = False
        self.connectors: list = []
