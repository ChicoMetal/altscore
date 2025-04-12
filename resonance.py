import requests

# Configurar los endpoints de la API
BASE_URL = "https://makers-challenge.altscore.ai"  # 🔹 Reemplaza con la URL real
GET_ENDPOINT = "/v1/s1/e2/resources/stars"
POST_ENDPOINT = "/v1/s1/e2/solution"

# Headers con API-KEY
HEADERS = {
    "API-KEY": "12f1eb55057742b080debc75751e8a47",  # 🔹 Reemplaza con tu API Key real
    "Content-Type": "application/json"
}

# Almacenar todas las resonancias
resonances = []
total_stars = 100  # 🔹 Ya sabemos que hay 100 estrellas
page = 1  # 🔹 Empezamos desde la primera página

# Hacer solicitudes hasta recolectar todas las estrellas
while len(resonances) < total_stars:
    response = requests.get(f"{BASE_URL}{GET_ENDPOINT}?page={page}", headers=HEADERS)
    
    if response.status_code != 200:
        print("❌ Error en la solicitud:", response.status_code, response.text)
        break

    data = response.json()  # 🔹 Convertir la respuesta a JSON
    
    if not data:  # 🔹 Si la API devuelve una lista vacía, hemos llegado al final
        print("⚠️ No hay más datos disponibles en la API.")
        break

    # Agregar las resonancias a la lista
    for star in data:
        resonances.append(star["resonance"])

    print(f"🌟 Página {page}: Recibidas {len(resonances)}/{total_stars} estrellas...")

    page += 1  # 🔹 Pasamos a la siguiente página

# Verificamos si logramos obtener todas las estrellas
if len(resonances) < total_stars:
    print("⚠️ No se obtuvieron todas las estrellas, puede haber un problema con la paginación.")
else:
    # Calcular la resonancia promedio
    average_resonance = round(sum(resonances) / len(resonances))
    print("average_resonance", resonances)
    # Enviar la respuesta
    solution = {"average_resonance": average_resonance}
    # post_response = requests.post(BASE_URL + POST_ENDPOINT, json=solution, headers=HEADERS)

    # print("✅ Respuesta del servidor:", post_response.status_code, post_response.text)