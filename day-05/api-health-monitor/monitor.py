import requests
import time
import logging
from config import URL, TIMEOUT, LATENCY_THRESHOLD, CHECK_INTERVAL


logging.basicConfig(
    filename="./logs/health.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)


def check_health(url):
    start = time.perf_counter()

    try:
        response = requests.get(url, timeout=TIMEOUT)

        latency = time.perf_counter() - start

        if response.status_code != 200:
            return {
                "status": "UNHEALTHY",
                "http_status": response.status_code,
                "latency": latency,
                "reason": f"HTTP {response.status_code}",
            }

        if latency >= LATENCY_THRESHOLD:
            return {
                "status": "UNHEALTHY",
                "http_status": response.status_code,
                "latency": latency,
                "reason": "Response too slow",
            }

        return {
            "status": "HEALTHY",
            "http_status": response.status_code,
            "latency": latency,
            "reason": None,
        }

    except requests.Timeout:
        return {
            "status": "UNHEALTHY",
            "http_status": None,
            "latency": None,
            "reason": "Request timed out",
        }

    except requests.RequestException as exc:
        return {
            "status": "UNHEALTHY",
            "http_status": None,
            "latency": None,
            "reason": str(exc),
        }


if __name__ == "__main__":
    while True:
        result = check_health(URL)
        latency = result.get("latency")
        latency_str = f"{latency:.3f}s" if latency is not None else "N/A"

        message = (
            f"status: {result['status']} | "
            f"HTTP: {result['http_status']} | "
            f"Latency: {latency_str} | "
            f"Reason: {result['reason']}"
        )

        if result["status"] == "HEALTHY":
            logging.info(message)
        else:
            logging.error(message)

        print(message)

        time.sleep(CHECK_INTERVAL)
