import requests
import base64

BASE_URL = "https://swapi.dev/api"
ORACLE_URL = "https://makers-challenge.altscore.ai/v1/s1/e3/resources/oracle-rolodex"
# SOLUTION_URL = "https://makers-challenge.altscore.ai/v1/s1/e3/solution"
HEADERS = {"API-KEY": "12f1eb55057742b080debc75751e8a47"}  # Agrega tu API Key aquí

def fetch_all_planets():
    planets = []
    url = f"{BASE_URL}/planets/"
    while url:
        response = requests.get(url)
        data = response.json()
        planets.extend(data["results"])
        url = data["next"]  # Manejo de paginación
    return planets

def fetch_character_alignment(name):
    response = requests.get(ORACLE_URL, params={"name": name}, headers=HEADERS)
    data = response.json()
    decoded_text = base64.b64decode(data["oracle_notes"]).decode("utf-8")
    return "Light" if "Light Side" in decoded_text else "Dark"

def calculate_ibf(planet, cache):
    light_count, dark_count = 0, 0
    total_count = len(planet["residents"])
    
    for resident_url in planet["residents"]:
        response = requests.get(resident_url)
        character = response.json()
        name = character["name"]
        
        # Usa caché para evitar llamadas repetidas al oráculo
        if name not in cache:
            cache[name] = fetch_character_alignment(name)

        if cache[name] == "Light":
            light_count += 1
        else:
            dark_count += 1

    if total_count == 0:
        return None  # Evita división por cero
    
    return (light_count - dark_count) / total_count

def find_balanced_planet():
    planets = fetch_all_planets()
    cache = {}  # Para almacenar respuestas del oráculo
    best_planet = None
    best_ibf = float("inf")

    for planet in planets:
        ibf = calculate_ibf(planet, cache)
        print("ibf", ibf, planet["name"])
        if ibf is not None and ibf == 0:  # Más cercano a 0
            best_ibf = ibf
            print("planet", planet)
            best_planet = planet["name"]

    return best_planet

# def submit_solution(planet_name):
    # response = requests.post(SOLUTION_URL, json={"planet_name": planet_name}, headers=HEADERS)
    # return response.json()

# Ejecutar el proceso
balanced_planet = find_balanced_planet()
print("result", balanced_planet)
# result = submit_solution(balanced_planet)
# print("Solution Response:", result)