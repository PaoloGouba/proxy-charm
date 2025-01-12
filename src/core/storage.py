def save_proxies_to_file(proxies, filename="output/proxies.txt"):
    """
    Salva la lista di proxy in un file .txt.
    """
    with open(filename, "w") as file:
        for proxy in proxies:
            file.write(f"{proxy['ip']}:{proxy['port']}\n")
    print(f"Proxies saved to {filename}")
