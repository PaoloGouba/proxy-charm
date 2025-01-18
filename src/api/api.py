from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import os

app = FastAPI()

class Proxy(BaseModel):
    ip: str
    port: str

PROXIES_FILE = "/Users/paologouba/Documents/Paolo/Goals/proxy-charm/output/proxies.txt"

@app.get("/proxies", response_model=List[Proxy])
def get_proxies():
    """
    Legge il file delle proxy e le restituisce in formato JSON.
    """
    if not os.path.exists(PROXIES_FILE):
        return []

    proxies = []
    with open(PROXIES_FILE, "r") as file:
        for line in file:
            try:
                ip, port = line.strip().split(":")
                proxies.append({"ip": ip, "port": port})
            except ValueError:
                continue  

    return proxies
