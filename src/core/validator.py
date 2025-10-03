from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
import time

class ProxyTester:
    # Primo endpoint super-leggero
    PRIMARY_URL = "https://icanhazip.com/"
    # Secondario solo in fallback
    SECONDARY_URL = "https://httpbin.org/ip"

    def __init__(self, proxy_ip, proxy_port, session: requests.Session | None = None):
        self.proxy = {
            "http": f"http://{proxy_ip}:{proxy_port}",
            "https": f"http://{proxy_ip}:{proxy_port}",
        }
        self.session = session or requests.Session()
        # timeouts separati: (connect, read)
        self.connect_timeout = 3
        self.read_timeout = 5

    def _get(self, url: str, timeout=None):
        to = timeout or (self.connect_timeout, self.read_timeout)
        return self.session.get(url, proxies=self.proxy, timeout=to)

    def test_once(self):
        # Prova PRIMARY
        try:
            r = self._get(self.PRIMARY_URL)
            if r.status_code == 200 and r.text.strip():
                return True, r.text.strip()
        except requests.RequestException:
            pass

        # Fallback SECONDARY
        try:
            r = self._get(self.SECONDARY_URL)
            if r.status_code == 200:
                return True, r.text[:64]
        except requests.RequestException:
            pass

        return False, None



def validate_proxies(proxies, repetitions: int = 1, max_threads: int = 80, save_rejected: bool = False):
    """
    Valida una lista di proxy più rapidamente:
    - Dedup già fatto a monte
    - Early-exit: 1 test basta; opzionale 2° test di conferma
    - Timeout aggressivi
    - Meno stampa, più throughput
    """
    if not proxies:
        return []

    # session condivisa per tenere vivo DNS/TLS quando possibile
    session = requests.Session()
    adapter = requests.adapters.HTTPAdapter(pool_connections=200, pool_maxsize=200, max_retries=0)
    session.mount("http://", adapter)
    session.mount("https://", adapter)

    def _task(p):
        tester = ProxyTester(p["ip"], p["port"], session=session)
        ok, info = tester.test_once()
        if not ok:
            return ("bad", p, "connect/timeout")
        if repetitions > 1:
            # opzionale: una seconda conferma molto rapida
            ok2, _ = tester.test_once()
            if not ok2:
                return ("bad", p, "unstable")
        return ("good", p, info)

    # limita thread a qualcosa di sensato
    workers = min(max_threads, max(8, len(proxies)))
    valid, rejected = [], []

    with ThreadPoolExecutor(max_workers=workers) as ex:
        futures = [ex.submit(_task, p) for p in proxies]
        done = 0
        for fut in as_completed(futures):
            status, proxy, info = fut.result()
            if status == "good":
                valid.append({"ip": proxy["ip"], "port": proxy["port"]})
            else:
                rejected.append(proxy)
            done += 1
            if done % 250 == 0:
                print(f"[VALIDATE] Progress {done}/{len(proxies)} — good:{len(valid)}")

    if save_rejected and rejected:
        with open("rejected_proxies.txt", "w") as f:
            for p in rejected:
                f.write(f"{p['ip']}:{p['port']}\n")
        print("[INFO] rejected_proxies.txt scritto")

    print(f"[RESULT] Valid: {len(valid)} / Total: {len(proxies)}")
    return valid
