import requests
import base64

session = requests.Session()

# Configurar los endpoints de la API
BASE_URL = "https://makers-challenge.altscore.ai"  # 🔹 Reemplaza con la URL real
POST_ENDPOINT = "/v1/s1/e8/actions/door"

# Headers con API-KEY
HEADERS = {
    "API-KEY": "12f1eb55057742b080debc75751e8a47",  # 🔹 Reemplaza con tu API Key real
    "Content-Type": "application/json"
}

def call_api():
    response = {}

    while "response" not in response or ("response" in response and response["response"] != "Has llegado al final. Recuerda usar el hechizo 'revelio' para descubrir el mensaje oculto."):
        post_response = session.post(BASE_URL + POST_ENDPOINT, json=None, headers=HEADERS)
        response = post_response.json()
        if post_response.status_code != 403:
            print("✅ Respuesta del servidor:", post_response.status_code, post_response.text)
            print("✅ Cookies ", session.cookies.get_dict())
            print("✅ Cookie gryffindor", base64.b64decode(session.cookies.get_dict()["gryffindor"]).decode("utf-8"))
            print("🚩🚩🚩🚩🚩🚩🚩🚩🚩🚩🚩🚩🚩🚩🚩🚩🚩🚩🚩🚩🚩🚩🚩")


if __name__ == "__main__":
    call_api()