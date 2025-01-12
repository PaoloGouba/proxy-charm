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
                print(f"Connettività OK: {response.json()}")
                return True
        except requests.exceptions.RequestException as e:
            print(f"Errore di connettività: {e}")
        return False

    def test_speed(self):
        """Misura il tempo di risposta del proxy."""
        try:
            start_time = time.time()
            response = requests.get(self.TEST_URL, proxies=self.proxy, timeout=5)
            if response.status_code == 200:
                latency = time.time() - start_time
                print(f"Velocità OK: {latency:.2f} secondi")
                return latency
        except requests.exceptions.RequestException as e:
            print(f"Errore di velocità: {e}")
        return None

    def test_anonymity(self):
        """Verifica se il proxy nasconde correttamente l'indirizzo IP."""
        try:
            response = requests.get(self.TEST_URL, proxies=self.proxy, timeout=5)
            if response.status_code == 200:
                visible_ip = response.json().get("origin")
                print(f"IP visibile tramite proxy: {visible_ip}")
                return visible_ip
        except requests.exceptions.RequestException as e:
            print(f"Errore di anonimato: {e}")
        return None

    def test_proxy(self, repetitions=3):
        """Esegue tutti i test per il proxy."""
        print(f"\nTesting proxy: {self.proxy['http']}")

        # Test connettività
        if not self.test_connectivity():
            print("Proxy non raggiungibile.")
            return {"status": "bad", "reason": "connectivity"}

        # Test velocità (media su più tentativi)
        latencies = []
        for _ in range(repetitions):
            latency = self.test_speed()
            if latency:
                latencies.append(latency)
            else:
                print("Errore durante il test di velocità.")
                return {"status": "bad", "reason": "speed"}
        avg_latency = sum(latencies) / len(latencies)
        print(f"Latenza media: {avg_latency:.2f} secondi")

        # Test anonimato
        visible_ip = self.test_anonymity()
        if not visible_ip:
            print("Errore durante il test di anonimato.")
            return {"status": "bad", "reason": "anonymity"}

        print("Proxy test completato con successo.")
        return {
            "status": "good",
            "average_latency": avg_latency,
            "visible_ip": visible_ip,
        }


# Esempio di utilizzo
if __name__ == "__main__":
    proxy_ip = "156.228.79.170"
    proxy_port = "3128"

    tester = ProxyTester(proxy_ip, proxy_port)
    result = tester.test_proxy()
    print("\nRisultato del test:", result)
