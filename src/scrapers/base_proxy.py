class BaseProxy():
    def __init__(self, url : str, port : int, location : str):
        self.url = url
        self.port = port
        self.location = location