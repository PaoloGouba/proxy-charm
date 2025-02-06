from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
import time


class ProxyTester:
    TEST_URLS = [
        "https://httpbin.org/ip",
        "https://icanhazip.com/",
        "https://ipinfo.io/ip"
    ]

    def __init__(self, proxy_ip, proxy_port):
        self.proxy = {
            "http": f"http://{proxy_ip}:{proxy_port}",
            "https": f"http://{proxy_ip}:{proxy_port}",
        }

    def test_connectivity(self, timeout=7):
        """
        Verifica se il proxy è raggiungibile con un timeout breve.
        """
        for url in self.TEST_URLS:
            try:
                response = requests.get(url, proxies=self.proxy, timeout=timeout)
                if response.status_code == 200:
                    return True
            except requests.exceptions.RequestException:
                continue
        return False

    def test_speed(self, timeout=10):
        """
        Misura il tempo di risposta del proxy con un timeout ottimizzato.
        """
        try:
            start_time = time.time()
            response = requests.get(self.TEST_URLS[0], proxies=self.proxy, timeout=timeout)
            if response.status_code == 200:
                return time.time() - start_time
        except requests.exceptions.RequestException:
            pass
        return None

    def test_anonymity(self, timeout=5):
        """
        Verifica se il proxy nasconde correttamente l'indirizzo IP.
        """
        try:
            response = requests.get(self.TEST_URLS[0], proxies=self.proxy, timeout=timeout)
            if response.status_code == 200:
                visible_ip = response.json().get("origin")
                return visible_ip
        except requests.exceptions.RequestException:
            pass
        return None

    def test_proxy(self, repetitions=3):
        """
        Esegue tutti i test per il proxy con timeout ottimizzati.
        """
        # Test connettività (timeout breve)
        if not self.test_connectivity(timeout=7):
            return {"status": "bad", "reason": "connectivity"}

        # Test velocità (media su più tentativi)
        latencies = []
        for _ in range(repetitions):
            latency = self.test_speed(timeout=10)
            if latency is not None:
                latencies.append(latency)
        if len(latencies) < repetitions // 2:  # Almeno metà dei tentativi devono riuscire
            return {"status": "bad", "reason": "speed"}
        avg_latency = sum(latencies) / len(latencies)

        # Test anonimato
        visible_ip = self.test_anonymity(timeout=5)
        if visible_ip is None:
            return {
                "status": "warning",
                "average_latency": avg_latency,
                "visible_ip": None,
            }

        return {
            "status": "good",
            "average_latency": avg_latency,
            "visible_ip": visible_ip,
        }


def validate_proxies(proxies, repetitions=3, save_rejected=True, max_threads=10):
    """
    Valida una lista di proxy utilizzando multi-threading e salva i risultati.
    """
    valid_proxies = []
    rejected_proxies = []

    def process_proxy(proxy):
        """
        Testa una singola proxy e restituisce il risultato.
        """
        tester = ProxyTester(proxy["ip"], proxy["port"])
        return proxy, tester.test_proxy(repetitions=repetitions)

    with ThreadPoolExecutor(max_threads) as executor:
        futures = [executor.submit(process_proxy, proxy) for proxy in proxies]

        for future in as_completed(futures):
            proxy, result = future.result()

            if result["status"] == "good":
                proxy_details = {
                    "ip": proxy["ip"],
                    "port": proxy["port"],
                    "latency": result["average_latency"],
                    "visible_ip": result["visible_ip"],
                }
                valid_proxies.append(proxy_details)
            elif result["status"] == "warning":
                print(f"Proxy accettata con avviso: {proxy['ip']}:{proxy['port']} (senza anonimato completo)")
                proxy_details = {
                    "ip": proxy["ip"],
                    "port": proxy["port"],
                    "latency": result["average_latency"],
                    "visible_ip": None,
                }
                valid_proxies.append(proxy_details)
            else:
                print(f"Proxy scartata: {proxy['ip']}:{proxy['port']} - Motivo: {result['reason']}")
                rejected_proxies.append(proxy)

    # Salva le proxy scartate in un file
    if save_rejected and rejected_proxies:
        with open("rejected_proxies.txt", "w") as file:
            for proxy in rejected_proxies:
                file.write(f"{proxy['ip']}:{proxy['port']}\n")
        print(f"Proxy scartate salvate in 'rejected_proxies.txt'.")

    return valid_proxies
