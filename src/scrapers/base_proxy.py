class BaseProxy:
    def __init__(self, ip, port, location=None):
        self.ip = ip
        self.port = port
        self.location = location or "Unknown"

    def __repr__(self):
        return f"Proxy(ip={self.ip}, port={self.port}, location={self.location})"
