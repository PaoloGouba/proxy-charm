import requests
import time

class ProxyTester:
    TEST_URL = "https://httpbin.org/ip"  # URL per testare l'indirizzo IP visibile

    def __init__(self, proxy_ip, proxy_port):
        self.proxy = {
            "http": f"http://{proxy_ip}:{proxy_port}",
            "https": f"http://{proxy_ip}:{proxy_port}",
        }

    def test_connectivity(self):
        """Verifica se il proxy è raggiungibile."""
        try:
            response = requests.get(self.TEST_URL, proxies=self.proxy, timeout=5)
            if response.status_code == 200:
                return True
        except requests.exceptions.RequestException:
            pass
        return False

    def test_speed(self):
        """Misura il tempo di risposta del proxy."""
        try:
            start_time = time.time()
            response = requests.get(self.TEST_URL, proxies=self.proxy, timeout=5)
            if response.status_code == 200:
                return time.time() - start_time
        except requests.exceptions.RequestException:
            pass
        return None

    def test_anonymity(self):
        """Verifica se il proxy nasconde correttamente l'indirizzo IP."""
        try:
            response = requests.get(self.TEST_URL, proxies=self.proxy, timeout=5)
            if response.status_code == 200:
                visible_ip = response.json().get("origin")
                return visible_ip
        except requests.exceptions.RequestException:
            pass
        return None

    def test_proxy(self, repetitions=3):
        """Esegue tutti i test per il proxy."""
        # Test connettività
        if not self.test_connectivity():
            return {"status": "bad", "reason": "connectivity"}

        # Test velocità (media su più tentativi)
        latencies = []
        for _ in range(repetitions):
            latency = self.test_speed()
            if latency is not None:
                latencies.append(latency)
            else:
                return {"status": "bad", "reason": "speed"}
        avg_latency = sum(latencies) / len(latencies)

        # Test anonimato
        visible_ip = self.test_anonymity()
        if not visible_ip:
            return {"status": "bad", "reason": "anonymity"}

        return {
            "status": "good",
            "average_latency": avg_latency,
            "visible_ip": visible_ip,
        }


def validate_proxies(proxies, repetitions=3):
    """
    Valida una lista di proxy e restituisce quelle valide con i dettagli.
    """
    valid_proxies = []
    for proxy in proxies:
        tester = ProxyTester(proxy["ip"], proxy["port"])
        result = tester.test_proxy(repetitions=repetitions)

        if result["status"] == "good":
            proxy_details = {
                "ip": proxy["ip"],
                "port": proxy["port"],
                "latency": result["average_latency"],
                "visible_ip": result["visible_ip"],
            }
            valid_proxies.append(proxy_details)
        else:
            print(f"Proxy scartata: {proxy['ip']}:{proxy['port']} - Motivo: {result['reason']}")

    return valid_proxies
