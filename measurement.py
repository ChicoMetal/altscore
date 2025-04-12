import requests
import time

# Configuración de la API
BASE_URL = "https://makers-challenge.altscore.ai"  # 🔹 Reemplaza con la URL real
GET_ENDPOINT = "/v1/s1/e1/resources/measurement"
POST_ENDPOINT = "/v1/s1/e1/solution"

HEADERS = {
    "API-KEY": "12f1eb55057742b080debc75751e8a47",  # 🔹 Reemplaza con tu API Key real
    "Content-Type": "application/json"
}

MAX_ATTEMPTS = 500  # 🔁 Número máximo de intentos
attempt = 0

while attempt < MAX_ATTEMPTS:
    response = requests.get(BASE_URL + GET_ENDPOINT, headers=HEADERS)
    data = response.json()

    # Verificar si los datos son válidos
    if "failed to measure" not in data["distance"] and "failed to measure" not in data["time"]:
        # Extract numeric values
        distance = float(data["distance"].split()[0])  # Extract number from "790 AU"
        time_value = float(data["time"].split()[0])  # Extract number from "1.9506... hours"

        # Calculate velocity
        velocity = round(distance / time_value)

        # Enviar la respuesta
        solution = {"speed": velocity}
        print("Solution: ", solution, data)
        post_response = requests.post(BASE_URL + POST_ENDPOINT, json=solution, headers=HEADERS)

        print("✅ Respuesta enviada con éxito:", post_response.status_code, post_response.text)
        break  # 🛑 Salir del bucle ya que obtuvimos datos válidos

    print(f"⚠️ Intento {attempt + 1}: Datos inválidos. Reintentando...", data)
    attempt += 1
    # time.sleep(1)  # ⏳ Esperar 2 segundos antes de intentar de nuevo

if attempt == MAX_ATTEMPTS:
    print("❌ No se pudo obtener una medición válida después de varios intentos.")