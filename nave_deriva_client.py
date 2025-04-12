import requests

def fetch_service_data():
    # URLs of the services
    urls = [
        ("GET", "https://0226-186-146-92-172.ngrok-free.app/status"),
        ("GET", "https://0226-186-146-92-172.ngrok-free.app/repair-bay"),
        ("POST", "https://0226-186-146-92-172.ngrok-free.app/teapot")
    ]

    for method, url in urls:
        try:
            response = None
            if method == "GET":
                response = requests.get(url)
            elif method == "POST":
                response = requests.post(url)

            response.raise_for_status()  # Raise an error for HTTP codes 4xx/5xx
            print(f"Response from {url}:")
            print(response.json() if response.headers.get('Content-Type') == 'application/json' else response.text)
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from {url}: {e}")

if __name__ == "__main__":
    fetch_service_data()